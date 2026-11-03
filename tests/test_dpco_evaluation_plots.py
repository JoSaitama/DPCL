"""Numerical provenance and real rendering checks for fixed-group seed curves."""

import csv
import importlib.util
from io import StringIO
import json
from pathlib import Path
import sys
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("dpco_group_plots", ROOT / "plots/plot_dpco_training.py")
plots = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = plots
SPEC.loader.exec_module(plots)


def write_csv(path, rows):
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def fixture(directory, offset_s=0, seed=None, method="adam", optimizer="adam"):
    directory.mkdir(parents=True)
    evaluation, groups = [], []
    for step, base_wall in ((0, 60), (10, 180), (20, 300)):
        wall = base_wall + offset_s
        evaluation.append(dict(step=step, samples_seen=step * 8, elapsed_wall_s=wall))
        # clean and corrupted are 6:2; wrong-label accuracy must be ignored.
        for group, count, accuracy, ce, label in (
            ("clean", 6, .5 + step / 80, 10 - wall / 60, "original"),
            ("corrupted_original", 2, 1., .3, "original"),
            ("corrupted_noisy", 2, 0., 7., "reference"),
        ):
            groups.append(dict(step=step, samples_seen=step * 8, group=group, label_source=label,
                               sample_count=count, ce=ce, top1=accuracy))
    write_csv(directory / "evaluation.csv", evaluation)
    write_csv(directory / "group_evaluation.csv", groups)
    if seed is not None:
        config = {"seed": seed, "training": {"optimizer": optimizer},
                  "method": {"name": method if method in ("adam", "sgd") else "dpco",
                             "negative_weight": 0 if method == "filter" else -1},
                  "reference": {"name": "ema", "beta": .9}}
        logs = directory.parent.parent / "logs" / directory.name
        logs.mkdir(parents=True)
        (logs / "metadata.json").write_text(json.dumps({"config": config}))
    return evaluation, groups


class EvaluationPlotTests(unittest.TestCase):
    def test_weighted_original_accuracy_smoothing_and_empty_corruption(self):
        with TemporaryDirectory() as tmp:
            directory = Path(tmp) / "run"
            _, groups = fixture(directory)
            run = plots.load_evaluation_run("adam", directory, 2)
            self.assertAlmostEqual(run.points[0]["raw_original_accuracy_percent"], 62.5)
            self.assertAlmostEqual(run.points[-1]["raw_original_accuracy_percent"], 81.25)
            self.assertAlmostEqual(run.points[1]["smooth_clean_ce"], 8.)
            self.assertAlmostEqual(run.points[-1]["smooth_clean_ce"], 6.)
            self.assertEqual(run.points[0]["wall_minutes"], 1.)
            # A genuinely empty corrupted group has blank metrics, not missing groups.
            for row in groups:
                if row["group"] != "clean":
                    row.update(sample_count=0, top1="", ce="")
            write_csv(directory / "group_evaluation.csv", groups)
            run = plots.load_evaluation_run("adam", directory)
            self.assertAlmostEqual(run.points[0]["raw_original_accuracy_percent"], 50.)

    def test_step_sample_sd_and_wall_overlap_interpolation(self):
        with TemporaryDirectory() as tmp:
            runs = []
            for method in plots.STYLES:
                for i in range(3):
                    path = Path(tmp) / f"{method}_{i}"
                    fixture(path, offset_s=30 * i)
                    runs.append(plots.load_evaluation_run(method, path))
            aggregate = plots.evaluation_aggregates(runs)
            first = aggregate["step"][0]
            self.assertAlmostEqual(first["raw_clean_ce_mean"], 8.5)
            self.assertAlmostEqual(first["raw_clean_ce_std"], .5)
            self.assertEqual(first["run_count"], 3)
            wall = [row for row in aggregate["time"] if row["method"] == "adam"]
            self.assertEqual([r["wall_minutes"] for r in wall], [2., 3., 3.5, 4., 5.])
            for row in wall:
                self.assertAlmostEqual(row["raw_clean_ce_mean"], 10 - row["wall_minutes"])
                self.assertAlmostEqual(row["raw_clean_ce_std"], 0.)
            with self.assertRaises(ValueError):
                plots.interpolate(runs[0].points, "wall_minutes", 0., "raw_clean_ce")

    def test_broken_group_join_units_and_population_are_rejected(self):
        for issue in ("missing", "duplicate", "wrong_labels", "counts", "percent", "nan", "seen", "time", "clean_empty"):
            with self.subTest(issue=issue), TemporaryDirectory() as tmp:
                path = Path(tmp) / "run"
                evaluation, groups = fixture(path)
                if issue == "missing":
                    groups.pop(1)
                elif issue == "duplicate":
                    groups.append(groups[0].copy())
                elif issue == "wrong_labels":
                    groups[1]["label_source"] = "reference"
                elif issue == "counts":
                    groups[-3]["sample_count"] = 7
                elif issue == "percent":
                    groups[0]["top1"] = 50
                elif issue == "nan":
                    groups[0]["ce"] = "nan"
                elif issue == "seen":
                    groups[0]["samples_seen"] = 8
                elif issue == "time":
                    evaluation[-1]["elapsed_wall_s"] = 180
                else:
                    groups[0]["sample_count"] = 0
                write_csv(path / "evaluation.csv", evaluation)
                write_csv(path / "group_evaluation.csv", groups)
                with self.assertRaises(ValueError):
                    plots.load_evaluation_run("adam", path)

    def test_unequal_nodes_duplicate_seeds_and_no_time_overlap_are_rejected(self):
        for issue in ("nodes", "seeds", "overlap"):
            with self.subTest(issue=issue), TemporaryDirectory() as tmp:
                runs = []
                for method in plots.STYLES:
                    for i in range(2):
                        path = Path(tmp) / "results/files" / f"{method}_repeat{i}"
                        fixture(path, seed=42 if issue == "seeds" else 42 + i, method=method)
                        runs.append(plots.load_evaluation_run(method, path))
                if issue == "nodes":
                    runs[1].points.pop()
                elif issue == "overlap":
                    for point in runs[1].points:
                        point["wall_minutes"] += 100
                with self.assertRaises(ValueError):
                    plots.evaluation_aggregates(runs)

    def test_metadata_seeds_are_allowed_to_differ_and_mislabels_fail(self):
        with TemporaryDirectory() as tmp:
            runs = []
            for method in plots.STYLES:
                for seed in (42, 43, 44):
                    path = Path(tmp) / "results/files" / f"{method}_adam_{seed}_run"
                    fixture(path, seed=seed, method=method)
                    runs.append(plots.load_evaluation_run(method, path))
            self.assertEqual(plots.evaluation_notes(runs), [])
            with self.assertRaises(ValueError):
                plots.load_evaluation_run("filter", runs[0].directory)
            metadata_path = runs[0].directory.parent.parent / "logs" / runs[0].directory.name / "metadata.json"
            metadata = json.loads(metadata_path.read_text())
            metadata["config"]["seed"] = 99
            metadata_path.write_text(json.dumps(metadata))
            with self.assertRaises(ValueError):
                plots.load_evaluation_run("adam", runs[0].directory)

    def test_nine_inputs_four_figures_csvs_integrity_and_cli_guards(self):
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            args, runs = [], []
            for method in plots.STYLES:
                for i in range(3):
                    path = root / "results/files" / f"{method}_adam_{42+i}_run"
                    fixture(path, offset_s=i * 30, seed=42+i, method=method)
                    runs.append(path)
                    args += [f"--{method}-dir", str(path)]
            originals = {p: p.read_bytes() for p in root.rglob("*.csv")}
            args += ["--plot-set", "clean-original", "--eval-smooth-window", "1", "--output-name", "groups", "--dpi", "70"]
            with patch.object(plots, "ROOT", root):
                output = plots.main(args)
                self.assertFalse(plt.rcParams['text.usetex'])
                self.assertEqual(plt.rcParams['font.family'], ['serif'])
                self.assertEqual(plt.rcParams['font.serif'], ['Nimbus Roman'])
                self.assertEqual(plt.rcParams['mathtext.fontset'], 'cm')
                self.assertEqual(len(list(output.glob("*.png"))), 4)
                self.assertEqual(len(list(output.glob("*.pdf"))), 4)
                manifest = json.loads((output / "plot_manifest.json").read_text())
                self.assertEqual(len(manifest["runs"]), 9)
                self.assertEqual(len(manifest["artifacts"]), 11)
                self.assertEqual(manifest["comparison_notes"], [])
                self.assertEqual(manifest["statistics"]["time_support_minutes"]["adam"], {"start": 2., "end": 5.})
                for path in output.glob("*.png"):
                    self.assertEqual(plt.imread(path).shape[:2], (315, 350))
                for path in output.glob("*.pdf"):
                    self.assertTrue(path.read_bytes().startswith(b"%PDF"))
                with (output / "evaluation_runs.csv").open() as handle:
                    rows = list(csv.DictReader(handle))
                self.assertEqual(len(rows), 27)
                self.assertEqual({row["seed"] for row in rows}, {"42", "43", "44"})
                for extra in ([], ["--time-axis", "active"], ["--eval-smooth-window", "0"],
                              ["--adam-dir", str(runs[0]), "--output-name", "duplicate"]):
                    with self.assertRaises(SystemExit), patch("sys.stderr", StringIO()):
                        plots.main(args + extra)
            self.assertTrue(all(path.read_bytes() == data for path, data in originals.items()))

    def test_figure_styles_uncertainty_and_missing_metadata_notes(self):
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        with TemporaryDirectory() as tmp:
            runs = []
            for method in plots.STYLES:
                path = Path(tmp) / method
                fixture(path)
                runs.append(plots.load_evaluation_run(method, path))
            data = plots.evaluation_aggregates(runs)
            notes = plots.evaluation_notes(runs)
            self.assertTrue(any("metadata.json" in note for note in notes))
            fig = plots.make_evaluation_figure(runs, data, "time", "original_accuracy_percent", "Time", "Acc", show_raw=False, plt=plt)
            try:
                fig.canvas.draw()
                ax = fig.axes[0]
                self.assertEqual(len(ax.collections), 3)
                self.assertEqual([line.get_color() for line in ax.lines], ["#1f77b4", "#d62728", "#ff7f0e"])
                self.assertEqual([line.get_linestyle() for line in ax.lines], ["-", "-", "--"])
                self.assertAlmostEqual(ax.get_window_extent().height / ax.get_window_extent().width, .9)
                self.assertEqual(ax.lines[0].get_xdata()[-1], 5.)
                self.assertEqual(ax.lines[0].get_ydata()[0], 62.5)
            finally:
                plt.close(fig)

    def test_sgd_three_seed_cli_statistics_labels_and_optimizer_guards(self):
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            args, runs = [], []
            for method in ("sgd", "flip", "filter"):
                for i, seed in enumerate((42, 43, 44)):
                    name = (f"mnist_noisy_mnist_cnn_sgd_{seed}_0.001_run" if method == "sgd" else
                            f"mnist_noisy_mnist_cnn_dpco_ema_b0.9_w{'-1' if method == 'flip' else '0'}_{seed}_0.001_run")
                    path = root / "results/files" / name
                    fixture(path, offset_s=i * 30, seed=seed, method=method, optimizer="sgd")
                    runs.append(plots.load_evaluation_run(method, path, optimizer="sgd"))
                    args.extend([f"--{method}-dir", str(path)])
            originals = {p: p.read_bytes() for p in root.rglob("*.csv")}
            aggregate = plots.evaluation_aggregates(runs)
            baseline = [r for r in aggregate['step'] if r['method'] == 'sgd']
            self.assertEqual(baseline[0]['run_count'], 3)
            self.assertAlmostEqual(baseline[0]['raw_clean_ce_mean'], 8.5)
            self.assertAlmostEqual(baseline[0]['raw_clean_ce_std'], .5)
            self.assertEqual(plots.evaluation_notes(runs), [])
            fig = plots.make_evaluation_figure(runs, aggregate, 'step', 'clean_ce', 'Step', 'CE', show_raw=False, plt=plt)
            try:
                labels = [t.get_text() for t in fig.axes[0].get_legend().get_texts()]
                self.assertEqual(labels, ['SGD (n=3)', 'DPCO Flip (n=3)', 'DPCO Filter (n=3)'])
                self.assertEqual(fig.axes[0].lines[0].get_color(), '#1f77b4')
            finally:
                plt.close(fig)
            args += ['--plot-set', 'clean-original', '--output-name', 'sgd_groups', '--formats', 'png', '--dpi', '70']
            with patch.object(plots, 'ROOT', root):
                output = plots.main(args)
                manifest = json.loads((output / 'plot_manifest.json').read_text())
                self.assertEqual(manifest['optimizer'], 'sgd')
                self.assertEqual(set(manifest['styles']), {'sgd', 'flip', 'filter'})
                self.assertEqual({r['seed'] for r in manifest['runs']}, {42, 43, 44})
                self.assertEqual({r['seed_source'] for r in manifest['runs']}, {'metadata'})
                self.assertEqual(len(list(output.glob('*.png'))), 4)
                self.assertNotIn('adam', manifest['statistics']['time_support_minutes'])
                with (output / 'evaluation_step_curves.csv').open() as handle:
                    self.assertEqual({r['method'] for r in csv.DictReader(handle)}, {'sgd', 'flip', 'filter'})
                # Accidentally providing two baselines is rejected by argparse.
                with self.assertRaises(SystemExit), patch('sys.stderr', StringIO()):
                    plots.main(args + ['--adam-dir', str(runs[0].directory)])
                # A single DPCO/Adam run cannot slip into an SGD comparison.
                path = root / 'results/logs' / runs[3].directory.name / 'metadata.json'
                metadata = json.loads(path.read_text())
                metadata['config']['training']['optimizer'] = 'adam'
                path.write_text(json.dumps(metadata))
                with self.assertRaises(SystemExit), patch('sys.stderr', StringIO()) as error:
                    plots.main(args + ['--output-name', 'mixed_optimizers'])
                self.assertIn('optimizer adam does not match requested sgd', error.getvalue())
                self.assertFalse((root / 'results/figures/mixed_optimizers').exists())
            self.assertTrue(all(p.read_bytes() == data for p, data in originals.items()))
            # Duplicate seeds remain invalid for the new baseline.
            runs[1].seed = runs[0].seed
            with self.assertRaisesRegex(ValueError, 'duplicate training seed'):
                plots.evaluation_aggregates(runs)

    def test_historical_sgd_names_without_metadata_and_wrong_baseline(self):
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            cases = [('sgd', 'mnist_noisy_mnist_cnn_sgd_42_0.001_run', 42),
                     ('flip', 'mnist_noisy_mnist_cnn_dpco_ema_b0.9_w-1_43_0.001_run', 43),
                     ('filter', 'mnist_noisy_mnist_cnn_dpco_ema_b0.9_w0_44_0.001_run', 44)]
            for method, name, seed in cases:
                path = root / name
                fixture(path)
                run = plots.load_evaluation_run(method, path, optimizer='sgd')
                self.assertEqual(run.seed, seed)
                self.assertEqual(run.seed_source, 'directory_name_unverified')
            with self.assertRaisesRegex(ValueError, 'directory optimizer sgd'):
                plots.load_evaluation_run('adam', root / cases[0][1])


if __name__ == "__main__":
    unittest.main()
