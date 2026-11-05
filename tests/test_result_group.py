"""Output grouping contracts for launch, recovery, and plotting."""

import json
from pathlib import Path
import subprocess
import sys
from tempfile import TemporaryDirectory
import unittest

from plots.plot_dpcl_training import load_metadata
from plots.plot_noise_training import identity
from src.config import load_config
from src.training.results import ResultsPaths

ROOT = Path(__file__).resolve().parents[1]
CONFIG = ROOT / "configs/tpu/digits/dpcl_adam.toml"


class ResultGroupTests(unittest.TestCase):
    def plan(self, *args, config=CONFIG):
        output = subprocess.check_output([sys.executable, str(ROOT / "scripts/run_suite.py"),
            "--config", str(config), "--dry-run", *args], text=True)
        return json.loads(output)

    def test_all_methods_and_seeds_share_inferred_or_explicit_group(self):
        methods = ("adam", "dpcl_flip", "dpcl_filter", "self_flip", "self_filter")
        for group, flags in (
                ("digit_k10", ("--bottom-k", "10")),
                ("digit_kpct10", ("--bottom-k-percent", "10")),
                ("digit_allneg", ()),
                ("my_experiment", ("--result-group", "my_experiment", "--bottom-k", "10"))):
            with self.subTest(group=group):
                plans = self.plan("--methods", *methods, "--seeds", "42", "43", *flags)
                self.assertEqual(len(plans), 10)
                self.assertEqual([p["seed"] for p in plans], [42] * 5 + [43] * 5)
                for p in plans:
                    self.assertEqual(p["result_group"], group)
                    command = p["command"]
                    self.assertEqual(command[command.index("--result-group") + 1], group)
                    name = command[command.index("--run-name") + 1]
                    for stream in ("files", "logs", "runs"):
                        self.assertEqual(Path(p[stream + "_dir"]),
                            ROOT / "results" / stream / group / name)
                self.assertIsNone(plans[0]["bottom_k"])
        adam = self.plan("--methods", "adam")
        self.assertEqual(adam["result_group"], "digit")

    def test_preset_budget_and_cli_precedence(self):
        with TemporaryDirectory() as tmp:
            preset = Path(tmp) / "preset.toml"
            preset.write_text(CONFIG.read_text().replace("negative_weight = -1.0",
                                                        "negative_weight = -1.0\nbottom_k = 6"))
            runs = self.plan("--methods", "adam", "dpcl_flip", config=preset)
            self.assertEqual([p["result_group"] for p in runs], ["digit_k6", "digit_k6"])
            plan = self.plan("--methods", "self_filter", "--bottom-k-percent", "10", config=preset)
            self.assertEqual(plan["result_group"], "digit_kpct10")

    def test_resume_legacy_and_grouped_without_moving_outputs(self):
        with TemporaryDirectory() as tmp:
            preset = Path(tmp) / "preset.toml"
            preset.write_text(CONFIG.read_text() + f'\n[results]\nroot_dir = "{tmp}"\n')
            flat = ResultsPaths(Path(tmp).resolve())
            grouped = ResultsPaths(Path(tmp).resolve(), "custom")
            legacy_run = flat.experiment("old_run")
            new_run = grouped.experiment("new_run")
            legacy_run.create()
            new_run.create()
            legacy = self.plan("--resume", "old_run", config=preset)
            self.assertIsNone(legacy["result_group"])
            self.assertNotIn("--result-group", legacy["command"])
            self.assertEqual(Path(legacy["files_dir"]), legacy_run.files)
            latest = self.plan("--resume", "new_run", config=preset)
            self.assertEqual(latest["result_group"], "custom")
            self.assertEqual(Path(latest["runs_dir"]), new_run.runs)
            grouped.experiment("old_run").create()
            with self.assertRaisesRegex(ValueError, "multiple locations"):
                flat.find_resume("old_run")
            explicit = self.plan("--resume", "old_run", "--result-group", "custom", config=preset)
            self.assertEqual(Path(explicit["files_dir"]), grouped.experiment("old_run").files)
            with self.assertRaises(ValueError):
                ResultsPaths(Path(tmp), "../escape")

    def test_plot_readers_use_mirrored_group_metadata(self):
        with TemporaryDirectory() as tmp:
            paths = ResultsPaths(Path(tmp), "digit_k10").experiment("digit_dpcl_ema_b0.5_w-1_k10_adam_42")
            paths.create()
            metadata = paths.logs / "metadata.json"
            metadata.write_text(json.dumps({"config": load_config(CONFIG).as_dict()}))
            sources = {}
            seed, beta, payload = identity("flip", paths.files, sources)
            self.assertEqual((seed, beta), (42, .5))
            self.assertIn(metadata, sources)
            sources = {}
            self.assertEqual(load_metadata("flip", paths.files, sources, optimizer="adam"), payload)
            self.assertIn(metadata, sources)
