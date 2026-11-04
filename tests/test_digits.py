"""Offline checks for acquisition, fixed splits, and the five-arm launcher."""

from dataclasses import replace
import gzip
import hashlib
from io import BytesIO
import json
from pathlib import Path
import subprocess
import sys
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import patch

import numpy as np

from src.config import load_config
from src.data.classification import open_training_images
from src.data import digits
from src.training.launch import resolve_config


ROOT = Path(__file__).resolve().parents[1]
CONFIG = ROOT / "configs/tpu/digits/dpcl_adam.toml"


class DigitsTests(unittest.TestCase):
    def test_verified_download_reuse_and_train_only_labels(self):
        raw = gzip.compress("".join(",".join([str(i % 17)] * 64 + [str(i % 10)]) + "\n"
                                    for i in range(digits.SAMPLE_COUNT)).encode())
        config = load_config(CONFIG).data
        with TemporaryDirectory() as tmp, patch.object(digits, "SOURCE_SHA256", hashlib.sha256(raw).hexdigest()):
            config = replace(config, prepared_dir=tmp)
            with self.assertRaises(FileNotFoundError):
                open_training_images(replace(config, download=False), ROOT)
            with patch("src.data.cifar100n_prepare.urllib.request.urlopen", return_value=BytesIO(raw)) as request:
                images, identity = open_training_images(config, ROOT)
                again, _ = open_training_images(config, ROOT)
            request.assert_called_once()
            self.assertEqual(images.fingerprint, again.fingerprint)
            self.assertEqual(images.counts, {"train": 1437, "validation": 360})
            self.assertEqual(identity["group_counts"], {"clean": 1150, "corrupted": 287})
            self.assertEqual(len(np.union1d(*images.indices.values())), 1797)
            self.assertEqual(len(np.intersect1d(*images.indices.values())), 0)
            i = int(images.group_indices["corrupted"][0])
            img, noisy = images.get("train", i)
            _, original = images.label_view("original").get("train", i)
            self.assertNotEqual(noisy, original)
            self.assertEqual(images.label_view("reference").get("train", i)[1], noisy)
            self.assertEqual(images.get("validation", 0)[1], images.indices["validation"][0] % 10)
            x = images.transform(img, 8)
            self.assertEqual(x.shape, (8, 8, 1))
            self.assertAlmostEqual(float(x[0, 0, 0]), (images.indices["train"][i] % 17) / 16)
            limited, _ = open_training_images(config, ROOT, limit=32)
            self.assertEqual(limited.counts, {"train": 32, "validation": 32})
            np.testing.assert_array_equal(limited.observed_labels, images.observed_labels)
            images.path.write_bytes(b"damaged")
            with self.assertRaisesRegex(ValueError, "checksum mismatch"):
                open_training_images(config, ROOT)

    def test_config_and_five_arm_dry_run(self):
        config = load_config(CONFIG)
        self.assertEqual(config.model.name, "digits_mlp")
        self.assertEqual(config.global_batch_size, 64)
        clean = resolve_config(CONFIG, mode="train", label_noise_percent=0)
        self.assertEqual(clean.data.mode, "clean")
        with self.assertRaisesRegex(ValueError, "Digits requires image_size=8"):
            resolve_config(CONFIG, mode="train", model="mnist_mlp")
        plans = json.loads(subprocess.check_output([sys.executable, str(ROOT / "scripts/run_suite.py"),
            "--config", str(CONFIG), "--methods", "adam", "dpcl_flip", "dpcl_filter", "self_flip", "self_filter",
            "--reference-beta", "0.5", "--dry-run"], text=True))
        self.assertEqual(len(plans), 5)
        self.assertTrue(all(p["dataset"] == "digits" and p["download_enabled"] for p in plans))
        self.assertEqual([p["reference_beta"] for p in plans], [None, .5, .5, 0., 0.])
