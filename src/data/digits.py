"""The sklearn Digits asset, with a fixed held-out split and train-only noise."""

import hashlib
import math
from pathlib import Path

import numpy as np
from PIL import Image

from src.data.cifar100n_prepare import canonical, download_asset, file_digest, preparation_lock
from src.data.mnist import _LabelView, corrupt_labels


SOURCE_URL = "https://raw.githubusercontent.com/scikit-learn/scikit-learn/1.7.2/sklearn/datasets/data/digits.csv.gz"
SOURCE_SHA256 = "09f66e6debdee2cd2b5ae59e0d6abbb73fc2b0e0185d2e1957e9ebb51e23aa22"
SAMPLE_COUNT, TEST_COUNT, SPLIT_SEED = 1797, 360, 42


def read_source(root, *, download=False, progress=None):
    root = Path(root).expanduser().resolve()
    path = root / "raw" / "digits.csv.gz"
    if download and not path.is_file():
        with preparation_lock(root):
            download_asset(SOURCE_URL, path, "sha256", SOURCE_SHA256, progress=progress)
    if not path.is_file():
        raise FileNotFoundError(f"Missing {path}; use --download or scripts/prepare_digits.py --stage download")
    if file_digest(path) != SOURCE_SHA256:
        raise ValueError(f"Digits source checksum mismatch: {path}")
    values = np.loadtxt(path, delimiter=",")
    if (values.shape != (SAMPLE_COUNT, 65) or not np.isfinite(values).all()
            or np.any(values != np.floor(values)) or np.any((values[:, :-1] < 0) | (values[:, :-1] > 16))
            or np.any((values[:, -1] < 0) | (values[:, -1] > 9))):
        raise ValueError("Invalid sklearn Digits pixel/label data")
    return path, values[:, :-1].astype(np.uint8).reshape(-1, 8, 8), values[:, -1].astype(np.int32)


def transform(image, image_size=8, *, rng=None):
    if image_size != 8 or image.size != (8, 8) or image.mode != "L":
        raise ValueError("Digits requires native 8x8 grayscale images")
    return np.asarray(image, np.float32)[..., None] / 16.


class DigitsImages:
    channels = 1
    transform = staticmethod(transform)

    def __init__(self, root, *, label_noise_percent=20., noise_seed=0, noise_percent=None,
                 download=False, limit=None, progress=None):
        if limit is not None and (isinstance(limit, bool) or not isinstance(limit, int) or limit <= 0):
            raise ValueError("Smoke sample limit must be a positive integer")
        self.path, self.pixels, labels = read_source(root, download=download, progress=progress)
        order = np.random.Generator(np.random.PCG64(SPLIT_SEED)).permutation(SAMPLE_COUNT)
        self.indices = {"train": np.sort(order[TEST_COUNT:]), "validation": np.sort(order[:TEST_COUNT])}
        self.full_counts = {split: len(ids) for split, ids in self.indices.items()}
        self.counts = {split: min(n, limit) if limit is not None else n for split, n in self.full_counts.items()}
        self.original_labels = labels[self.indices["train"]]
        self.test_labels = labels[self.indices["validation"]]
        self.observed_labels = corrupt_labels(self.original_labels, label_noise_percent, noise_seed)
        self.reference_labels = self.observed_labels
        corrupted = self.observed_labels != self.original_labels
        actual = 100 * float(np.mean(corrupted))
        if noise_percent is not None and not math.isclose(noise_percent, actual, rel_tol=0, abs_tol=1e-8):
            raise ValueError(f"noise_percent checks actual rate: loaded {actual}%")
        active = corrupted[:self.counts["train"]]
        self.group_indices = {"clean": np.flatnonzero(~active), "corrupted": np.flatnonzero(active)}
        self.identity = {"dataset": "digits", "source_url": SOURCE_URL, "source_sha256": SOURCE_SHA256,
            "split_algorithm": "PCG64_permutation_first360_test_sort_each_v1", "split_seed": SPLIT_SEED,
            "split_sha256": {key: hashlib.sha256(ids.astype("<i4").tobytes()).hexdigest()
                             for key, ids in self.indices.items()},
            "noise_type": "symmetric_exclude_original_exact_count", "noise_seed": noise_seed,
            "label_noise_percent": label_noise_percent, "actual_noise_percent": actual,
            "corruption_algorithm": "numpy_default_rng_permutation_then_all_offsets_v1; round_half_up_count",
            "mismatch_count": int(corrupted.sum()), "active_mismatch_count": int(active.sum()),
            "observed_labels_sha256": hashlib.sha256(self.observed_labels.astype("<i4").tobytes()).hexdigest(),
            "full_counts": self.full_counts, "view_counts": self.counts,
            "group_counts": {key: len(ids) for key, ids in self.group_indices.items()},
            "evaluation_split": "fixed_digits_held_out_test_no_model_selection"}
        self.fingerprint = hashlib.sha256(canonical(self.identity)).hexdigest()
        for array in (self.pixels, self.original_labels, self.test_labels, self.observed_labels,
                      *self.indices.values(), *self.group_indices.values()):
            array.flags.writeable = False

    def get(self, split, index):
        if split not in self.counts or not 0 <= index < self.counts[split]:
            raise IndexError(f"Digits image outside configured view: {split}/{index}")
        labels = self.observed_labels if split == "train" else self.test_labels
        return Image.fromarray(self.pixels[self.indices[split][index]]), int(labels[index])

    def label_view(self, kind):
        if kind not in ("original", "reference"):
            raise ValueError("Unknown Digits label view")
        return _LabelView(self, kind)

    def close(self):
        # This dataset is held entirely in memory; there are no open handles.
        pass
