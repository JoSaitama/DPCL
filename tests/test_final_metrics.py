"""Tests for the final report artifact without a JAX runtime."""

import json
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from src.training.recording import FINAL_METRICS_FILE, write_final_metrics


class FinalMetricsTests(unittest.TestCase):
    def write(self, directory, rows):
        write_final_metrics(directory, dict(step=2200, val_ce=.36, val_top1=.9138,
            eval_sample_count=360), rows, samples_seen=140800,
            evaluation_mode="fixed_digits_held_out_test", execution_mode="train")

    def test_distinct_label_views_and_clean_splits(self):
        rows = [dict(group="clean", ce=.21, sample_count=1150),
                dict(group="corrupted_original", ce=.91, sample_count=287),
                dict(group="corrupted_noisy", ce=1.97, sample_count=287)]
        with TemporaryDirectory() as tmp:
            directory = Path(tmp)
            csv_path = directory / "evaluation.csv"
            csv_path.write_text("step,val_ce\n2200,0.36\n")
            self.write(directory, rows)
            data = json.loads((directory / FINAL_METRICS_FILE).read_text())
            self.assertEqual(data["step"], 2200)
            self.assertEqual(data["metrics"], dict(clean_test_ce=.36, test_acc=.9138,
                corrupt_true_ce=.91, corrupt_wrong_ce=1.97))
            self.assertEqual(data["clean_train_ce"], .21)
            self.assertEqual(data["sample_counts"], dict(held_out=360, clean_train=1150,
                corrupted_train=287))
            self.assertEqual(csv_path.read_text(), "step,val_ce\n2200,0.36\n")

    def test_missing_or_empty_corrupted_labels(self):
        clean = dict(group="clean", ce=.21, sample_count=1437)
        wrong = dict(group="corrupted_noisy", ce=None, sample_count=0)
        true = dict(group="corrupted_original", ce=None, sample_count=0)
        with TemporaryDirectory() as tmp:
            directory = Path(tmp)
            report = directory / FINAL_METRICS_FILE
            self.write(directory, [clean, wrong])
            self.assertFalse(report.exists())
            with self.assertRaisesRegex(ValueError, "same sample count"):
                self.write(directory, [clean, wrong, dict(true, sample_count=1)])
            self.assertFalse(report.exists())
            self.write(directory, [clean, wrong, true])
            data = json.loads(report.read_text())
            self.assertIsNone(data["metrics"]["corrupt_true_ce"])
            self.assertIsNone(data["metrics"]["corrupt_wrong_ce"])
