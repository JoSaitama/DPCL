"""Reproducibly retain a fixed number of released human annotation errors.

This creates a derived benchmark, not another official CIFAR-100N release.
No new erroneous targets are generated; source images and labels stay untouched.
"""

import hashlib
import math
from pathlib import Path

import numpy as np

from src.data.cifar100n_prepare import (
    labels_vector, preparation_lock, publish_arrays, verify_prepared,
)

VARIANT = "controlled_human_error_retention"


def _read_arrays(directory, manifest):
    """Validate semantic content as well as the hashes checked by verify_prepared."""
    prepared = directory / "prepared"
    with np.load(prepared / "labels.npz", allow_pickle=False) as labels:
        count = manifest["counts"]["train"]
        test_count = manifest["counts"]["validation"]
        clean = labels_vector(labels["clean_label"], count, name="clean_label")
        human = labels_vector(labels["noise_label"], count, name="noise_label")
        test = labels_vector(labels["test_label"], test_count, name="test_label")
    images = []
    try:
        for name, size in (("train_images.npy", count), ("test_images.npy", test_count)):
            pixels = np.load(prepared / name, mmap_mode="r", allow_pickle=False)
            images.append(pixels)
            if size <= 0 or pixels.shape != (size, 32, 32, 3) or pixels.dtype != np.uint8:
                raise ValueError(f"Invalid CIFAR images: {name}")
        mismatches = int(np.count_nonzero(clean != human))
        rate = 100 * float(np.mean(clean != human))
        if (manifest["human_mismatch_count"] != mismatches
                or not math.isclose(manifest["human_noise_percent"], rate, abs_tol=1e-10)):
            raise ValueError("CIFAR label counts disagree with manifest")
    except Exception:
        _close_images(images)
        raise
    return images, (clean, human, test)


def _close_images(images):
    for pixels in images:
        pixels._mmap.close()


def prepare_controlled(source_dir, output_dir, *, target_noise_percent, selection_seed=0):
    """Build/reuse an independent cache, rounding target counts half upward.

    Select uniformly without replacement from source mismatches using PCG64.
    Selection is global, not stratified by class, and independent of training RNG.
    Old one-off controlled caches are reused after the same identity/content checks.
    """
    source = Path(source_dir).expanduser().resolve()
    output = Path(output_dir).expanduser().resolve()
    if source == output or source in output.parents or output in source.parents:
        raise ValueError("Source and output must be separate, non-nested directories")
    if (isinstance(target_noise_percent, (bool, np.bool_))
            or not isinstance(target_noise_percent, (int, float, np.integer, np.floating))
            or not math.isfinite(target_noise_percent) or not 0 <= target_noise_percent <= 100):
        raise ValueError("target_noise_percent must be finite and between 0 and 100")
    if (isinstance(selection_seed, (bool, np.bool_))
            or not isinstance(selection_seed, (int, np.integer)) or selection_seed < 0):
        raise ValueError("selection_seed must be a nonnegative integer")
    target_noise_percent, selection_seed = float(target_noise_percent), int(selection_seed)
    base, base_sha = verify_prepared(source)
    if base["provenance"].get("variant") == VARIANT:
        raise ValueError("Use the original human-label cache as source, not a controlled derivative")
    images, (clean, human, test) = _read_arrays(source, base)
    try:
        bad = np.flatnonzero(clean != human)
        available = 100 * float(np.mean(clean != human))
        if target_noise_percent > available:
            raise ValueError(f"Target {target_noise_percent}% exceeds source human noise {available}%")
        count = int(math.floor(len(clean) * target_noise_percent / 100 + 0.5))
        # Explicit PCG64 matches the earlier default_rng recipe and pins the bit generator.
        rng = np.random.Generator(np.random.PCG64(selection_seed))
        keep = np.sort(rng.choice(bad, count, replace=False))
        observed = clean.copy()
        observed[keep] = human[keep]
        identity = {
            "variant": VARIANT,
            "source_manifest_sha256": base_sha,
            "selection_seed": selection_seed,
            "target_noise_percent": target_noise_percent,
            "retained_indices_sha256": hashlib.sha256(keep.astype("<i8").tobytes()).hexdigest(),
        }
        provenance = {
            **identity, "dataset": "cifar100n",
            "official_revision": base["provenance"].get("official_revision"),
            "source_directory": str(source),
            "selection_rng": "numpy.default_rng/PCG64", "numpy_version": np.__version__,
            "original_human_error_count": len(bad), "retained_error_count": count,
            "restored_error_count": len(bad) - count,
            "target_count_rule": "floor(train_count * target_noise_percent / 100 + 0.5)",
            "selection_scope": "global_uniform_without_replacement",
        }
        with preparation_lock(output):
            if (output / "prepared").exists():
                manifest, digest = verify_prepared(output)
                if any(manifest["provenance"].get(k) != v for k, v in identity.items()):
                    raise ValueError("Existing controlled cache has a different source/rate/seed/selection")
                if any(manifest["files"][name] != base["files"][name]
                       for name in ("train_images.npy", "test_images.npy")):
                    raise ValueError("Existing controlled cache images differ from source")
                cached_images, cached_labels = _read_arrays(output, manifest)
                try:
                    if not all(np.array_equal(a, b) for a, b in
                               zip(cached_labels, (clean, observed, test))):
                        raise ValueError("Existing controlled cache labels differ from expected selection")
                finally:
                    _close_images(cached_images)
                return manifest, digest
            if any(path.name != ".prepare.lock" for path in output.iterdir()):
                raise FileExistsError("Output is not empty; preserve it and choose another directory")
            return publish_arrays(output, images[0], clean, observed, images[1], test, provenance)
    finally:
        _close_images(images)
