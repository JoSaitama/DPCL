"""Controlled human-label retention, immutable artifacts and training-reader compatibility."""

import hashlib
import json
from pathlib import Path
import subprocess
import sys
from tempfile import TemporaryDirectory
import unittest

import numpy as np

from src.data.cifar100n import CIFAR100NImages
from src.data.cifar100n_controlled import prepare_controlled
from src.data.cifar100n_prepare import publish_arrays, verify_prepared

ROOT = Path(__file__).resolve().parents[1]


class ControlledHumanNoiseTests(unittest.TestCase):
    def setUp(self):
        self.temporary = TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.source, self.output = self.root / "source", self.root / "human20_s0"
        self.clean = np.arange(10, dtype=np.int32)
        self.human = self.clean.copy()
        self.human[[1, 3, 5, 7]] += 1
        self.images = np.random.default_rng(17).integers(0, 256, (10, 32, 32, 3), dtype=np.uint8)
        self.base, self.base_sha = publish_arrays(self.source, self.images, self.clean, self.human,
            self.images[:2], self.clean[:2], {"official_revision": "fixture", "dataset": "fixture"})

    def prepare(self, **kwargs):
        return prepare_controlled(self.source, self.output, target_noise_percent=20, **kwargs)

    def labels(self, root):
        with np.load(root / "prepared/labels.npz", allow_pickle=False) as record:
            return {key: record[key].copy() for key in record.files}

    def snapshot(self, root):
        return {str(p.relative_to(root)): hashlib.sha256(p.read_bytes()).hexdigest()
                for p in root.rglob("*") if p.is_file()}

    def test_exact_global_rate_preserves_targets_images_originals_and_source(self):
        before = self.snapshot(self.source)
        manifest, digest = self.prepare()
        labels = self.labels(self.output)
        keep = np.flatnonzero(labels["clean_label"] != labels["noise_label"])
        np.testing.assert_array_equal(keep, np.sort(np.random.default_rng(0).choice([1, 3, 5, 7], 2, replace=False)))
        np.testing.assert_array_equal(labels["clean_label"], self.clean)
        np.testing.assert_array_equal(labels["noise_label"][keep], self.human[keep])
        np.testing.assert_array_equal(labels["test_label"], self.clean[:2])
        self.assertEqual(manifest["human_mismatch_count"], 2)
        self.assertEqual(manifest["human_noise_percent"], 20)
        self.assertEqual(manifest["provenance"]["restored_error_count"], 2)
        for name in ("train_images.npy", "test_images.npy"):
            self.assertEqual(manifest["files"][name], self.base["files"][name])
        self.assertEqual(verify_prepared(self.output)[1], digest)
        self.assertEqual(self.snapshot(self.source), before)
        data = CIFAR100NImages(self.output, noise_type="noisy100", is_human=True,
                              noise_percent=20, download=False)
        try:
            np.testing.assert_array_equal(data.original_labels, self.clean)
            np.testing.assert_array_equal(data.observed_labels, labels["noise_label"])
            self.assertEqual(len(data.group_indices["clean"]), 8)
            self.assertEqual(len(data.group_indices["corrupted"]), 2)
        finally:
            data.close()
        with self.assertRaises(ValueError):
            CIFAR100NImages(self.source, noise_percent=20, download=False)

    def test_repeated_request_reuses_without_rewriting_and_conflicts_fail(self):
        manifest, digest = self.prepare()
        before = self.snapshot(self.output)
        self.assertEqual(self.prepare(), (manifest, digest))
        self.assertEqual(self.snapshot(self.output), before)
        for rate, seed in ((10, 0), (20, 1)):
            with self.subTest(rate=rate, seed=seed), self.assertRaises(ValueError):
                prepare_controlled(self.source, self.output, target_noise_percent=rate, selection_seed=seed)
        self.assertEqual(self.snapshot(self.output), before)

    def test_independent_caches_reproduce_selection_and_seed_changes_it(self):
        first, _ = self.prepare()
        for name, seed in (("same", 0), ("other", 1)):
            destination = self.root / name
            manifest, _ = prepare_controlled(self.source, destination,
                target_noise_percent=20, selection_seed=seed)
            identical = (manifest["provenance"]["retained_indices_sha256"]
                         == first["provenance"]["retained_indices_sha256"])
            self.assertEqual(identical, seed == 0)

    def test_zero_full_source_and_count_rounding(self):
        for rate, count, actual in ((0, 0, 0), (40, 4, 40), (15, 2, 20)):
            with self.subTest(rate=rate):
                manifest, _ = prepare_controlled(self.source, self.root / str(rate),
                    target_noise_percent=rate)
                self.assertEqual(manifest["human_mismatch_count"], count)
                self.assertEqual(manifest["human_noise_percent"], actual)
                self.assertEqual(manifest["provenance"]["target_noise_percent"], rate)

    def test_invalid_inputs_do_not_create_a_destination(self):
        for rate in (True, float("nan"), float("inf"), -1, 40.01, 100.1, "20"):
            with self.subTest(rate=rate), self.assertRaises(ValueError):
                prepare_controlled(self.source, self.output, target_noise_percent=rate)
        for seed in (-1, True, 0.5):
            with self.subTest(seed=seed), self.assertRaises(ValueError):
                self.prepare(selection_seed=seed)
        self.assertFalse(self.output.exists())

    def test_source_destination_overlap_and_derivative_source_are_rejected(self):
        for destination in (self.source, self.source / "child", self.root):
            with self.subTest(destination=destination), self.assertRaises(ValueError):
                prepare_controlled(self.source, destination, target_noise_percent=20)
        self.prepare()
        with self.assertRaisesRegex(ValueError, "original human-label"):
            prepare_controlled(self.output, self.root / "nested_derivative", target_noise_percent=10)

    def test_incomplete_or_corrupt_output_is_preserved(self):
        self.output.mkdir()
        marker = self.output / "unfinished.txt"
        marker.write_text("preserve")
        with self.assertRaises(FileExistsError):
            self.prepare()
        self.assertEqual(marker.read_text(), "preserve")
        other = self.root / "corrupt"
        prepare_controlled(self.source, other, target_noise_percent=20)
        (other / "prepared/labels.npz").write_bytes(b"damaged")
        before = self.snapshot(other)
        with self.assertRaisesRegex(ValueError, "checksum"):
            prepare_controlled(self.source, other, target_noise_percent=20)
        self.assertEqual(self.snapshot(other), before)

    def test_existing_one_off_cache_is_accepted_but_wrong_content_is_not(self):
        manifest, _ = self.prepare()
        labels = self.labels(self.output)
        old_provenance = {key: value for key, value in manifest["provenance"].items()
                          if key not in ("target_count_rule", "selection_scope")}
        for name, observed in (("legacy", labels["noise_label"]), ("wrong", self.human)):
            destination = self.root / name
            old, digest = publish_arrays(destination, self.images, self.clean, observed,
                self.images[:2], self.clean[:2], old_provenance)
            before = self.snapshot(destination)
            if name == "legacy":
                self.assertEqual(prepare_controlled(self.source, destination,
                    target_noise_percent=20), (old, digest))
            else:
                with self.assertRaisesRegex(ValueError, "labels differ"):
                    prepare_controlled(self.source, destination, target_noise_percent=20)
            # Lock creation is expected; no prepared data is rewritten.
            self.assertEqual({k: v for k, v in self.snapshot(destination).items() if k != ".prepare.lock"}, before)

    def test_cli_prepares_verifies_and_requires_explicit_generation_arguments(self):
        script = str(ROOT / "scripts/prepare_cifar100n.py")
        command = [sys.executable, script]
        result = subprocess.run(command + ["--stage", "controlled", "--source-dir", str(self.source),
            "--output-dir", str(self.output), "--target-noise-percent", "20", "--selection-seed", "0"],
            capture_output=True, text=True, check=True, cwd=ROOT)
        record = json.loads(result.stdout)
        self.assertEqual(record["event"], "controlled_human_ready")
        self.assertEqual(record["human_noise_percent"], 20)
        verified = subprocess.run(command + ["--stage", "verify", "--output-dir", str(self.output)],
            capture_output=True, text=True, check=True, cwd=ROOT)
        self.assertEqual(json.loads(verified.stdout)["manifest_sha256"], record["manifest_sha256"])
        for arguments in (["--stage", "controlled", "--target-noise-percent", "20"],
                          ["--stage", "controlled", "--output-dir", str(self.output)],
                          ["--stage", "verify", "--target-noise-percent", "20"]):
            failed = subprocess.run(command + arguments, capture_output=True, text=True, cwd=ROOT)
            self.assertEqual(failed.returncode, 2)


if __name__ == "__main__":
    unittest.main()
