"""Validate renamed MNIST cache compatibility without a training runtime."""

import hashlib
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import patch

import numpy as np

from src.data.mnist import MNISTImages
from src.data.mnist_prepare import FORMAT, prepare, publish_arrays, verify_prepared


def publish(root, version):
    with patch("src.data.mnist_prepare.FORMAT", version):
        return publish_arrays(root, np.zeros((10, 28, 28), np.uint8), np.arange(10),
            np.ones((2, 28, 28), np.uint8), np.array([2, 3]), {"dataset": "test_fixture"})


def hashes(directory):
    return {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in directory.iterdir()}


class MNISTCacheCompatibilityTests(unittest.TestCase):
    def test_old_and_current_caches_reuse_original_files_and_digest(self):
        for version in ("dpco-mnist-v1", FORMAT):
            with self.subTest(version=version), TemporaryDirectory() as tmp:
                directory = Path(tmp) / "prepared"
                manifest, digest = publish(tmp, version)
                before = hashes(directory)
                self.assertEqual(verify_prepared(tmp), (manifest, digest))
                with patch("urllib.request.urlopen", side_effect=AssertionError("must not download")):
                    reader = MNISTImages(tmp, download=True, label_noise_percent=20., noise_seed=0)
                    try:
                        self.assertEqual(reader.counts, {"train": 10, "validation": 2})
                        self.assertEqual(reader.identity["manifest_sha256"], digest)
                        self.assertEqual(reader.identity["active_mismatch_count"], 2)
                        self.assertEqual(reader.get("validation", 0)[1], 2)
                    finally:
                        reader.close()
                self.assertEqual(hashes(directory), before)

    def test_legacy_completion_and_payload_integrity_still_checked(self):
        for name, message in (("complete.json", "identity mismatch"),
                              ("train_images.npy", "checksum mismatch")):
            with self.subTest(name=name), TemporaryDirectory() as tmp:
                publish(tmp, "dpco-mnist-v1")
                target = Path(tmp) / "prepared" / name
                target.write_bytes(b"{}")
                with self.assertRaisesRegex(ValueError, message):
                    prepare(tmp, download=True)

    def test_unknown_format_rejected_even_if_manifest_hash_matches(self):
        with TemporaryDirectory() as tmp:
            publish(tmp, "unknown-mnist-v1")
            with self.assertRaisesRegex(ValueError, "identity mismatch"):
                verify_prepared(tmp)
