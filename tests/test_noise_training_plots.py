"""Scientific grouping, smoothing, provenance and CPU rendering checks."""

import csv
import importlib.util
import json
from pathlib import Path
import sys
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import patch
from io import StringIO


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("noise_training_plots", ROOT / "plots/plot_noise_training.py")
plots = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = plots
SPEC.loader.exec_module(plots)


def write_csv(path, data):
    plots.csv_write(path, data)


def fixture(root, method, beta=None, counts=(8, 2), seed=42):
    suffix = f"dpco_ema_b{beta}_w{'-1' if method == 'flip' else '0'}_" if beta is not None else ""
    directory = root / "files" / f"noise{counts[1]}" / f"test_{suffix}adam_{seed}"
    directory.mkdir(parents=True)
    write_csv(directory / "evaluation.csv", [dict(step=s, samples_seen=s * 8, val_top1=.1 + s / 10)
                                             for s in (0, 2, 4)])
    groups = []
    for step in (0, 2, 4):
        for group, count, acc in (("clean", counts[0], .2 + step / 10),
                                  ("corrupted_original", counts[1], .4 - step / 20),
                                  ("corrupted_noisy", counts[1], .1 + step / 20)):
            groups.append(dict(step=step, samples_seen=step * 8, group=group,
                               label_source=plots.GROUPS[group], sample_count=count, top1=acc))
    write_csv(directory / "group_evaluation.csv", groups)
    if method != "adam":
        write_csv(directory / "dpco_steps.csv", [dict(step=s, valid_batch_size=8,
                  dpco_negative_count=s, dpco_edited_count=s, dpco_negative_weight=-1 if method == "flip" else 0)
                  for s in range(1, 5)])
    return directory


def all_fixtures(root):
    inputs, runs = [], []
    for counts in ((8, 2), (6, 4)):
        for method in plots.STYLES:
            for beta in ((None,) if method == "adam" else (.95, .96, .98)):
                directory = fixture(root, method, beta, counts)
                inputs.extend([f"--{method}-dir", str(directory)])
                runs.append(plots.load_run(method, directory))
    return inputs, runs


class NoiseTrainingPlotTests(unittest.TestCase):
    def test_sample_weighted_smoothing_before_stride(self):
        series = list(plots.edit_series([(1, 0, 2), (2, 8, 8), (3, 0, 2)], 2))
        self.assertEqual(series, [(1, 0., 0.), (2, 100., 80.), (3, 0., 80.)])
        self.assertEqual(list(plots.trailing([10, 30, 50], 2)), [10, 20, 40])

    def test_noise_groups_beta_pairing_and_raw_endpoint(self):
        with TemporaryDirectory() as tmp:
            _, runs = all_fixtures(Path(tmp))
            cohorts, betas, endpoint = plots.comparison(runs, .96)
            self.assertEqual([c['adam', None].noise_percent for c in cohorts], [20., 40.])
            self.assertEqual(betas, [.95, .96, .98])
            self.assertEqual(endpoint, 4)
            self.assertAlmostEqual(cohorts[0]['flip', .98].points[-1]['original_accuracy'], 20.)
            self.assertEqual(plots.comparison(runs, .96, 2)[2], 2)
            with self.assertRaisesRegex(ValueError, 'exact recorded'):
                plots.comparison(runs, .96, 3)
            with self.assertRaisesRegex(ValueError, 'Duplicate'):
                plots.comparison(runs + [runs[0]], .96)
            with self.assertRaisesRegex(ValueError, 'matching'):
                plots.comparison(runs[:-1], .96)
            runs[-1].seed = 43
            with self.assertRaisesRegex(ValueError, 'common training seed'):
                plots.comparison(runs, .96)

    def test_reject_misaligned_groups_and_corruption_labels(self):
        with TemporaryDirectory() as tmp:
            directory = fixture(Path(tmp), 'flip', .96)
            path = directory / 'group_evaluation.csv'
            with path.open() as handle:
                data = list(csv.DictReader(handle))
            data[-1]['label_source'] = 'original'
            write_csv(path, data)
            with self.assertRaisesRegex(ValueError, 'label_source'):
                plots.load_run('flip', directory)
            data[-1]['label_source'] = 'reference'
            data[-1]['samples_seen'] = '31'
            write_csv(path, data)
            with self.assertRaisesRegex(ValueError, 'misaligned'):
                plots.load_run('flip', directory)
            data[-1]['samples_seen'] = '32'
            data[-1]['top1'] = '0.9'
            write_csv(path, data)
            with self.assertRaisesRegex(ValueError, 'sum above'):
                plots.load_run('flip', directory)

    def test_nested_metadata_and_method_weight_validation(self):
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            directory = fixture(root, 'flip', .96)
            logs = root / 'logs' / directory.name
            logs.mkdir(parents=True)
            metadata = dict(config=dict(seed=42, training=dict(optimizer='adam'),
                                       method=dict(name='dpco', negative_weight=-1),
                                       reference=dict(name='ema', beta=.96)))
            path = logs / 'metadata.json'
            path.write_text(json.dumps(metadata))
            run = plots.load_run('flip', directory)
            self.assertIsNotNone(run.metadata)
            self.assertIn(path.resolve(), run.sources)
            metadata['config']['reference']['beta'] = .95
            path.write_text(json.dumps(metadata))
            with self.assertRaisesRegex(ValueError, 'betas disagree'):
                plots.load_run('flip', directory)

    def test_reject_incomplete_updates_and_invalid_edit_counts(self):
        with TemporaryDirectory() as tmp:
            directory = fixture(Path(tmp), 'filter', .96)
            with self.assertRaisesRegex(ValueError, 'filename weight'):
                plots.load_run('flip', directory, load_edits=False)
            with self.assertRaisesRegex(ValueError, 'Adam baseline'):
                plots.load_run('adam', directory, load_edits=False)
            path = directory / 'dpco_steps.csv'
            with path.open() as handle:
                data = list(csv.DictReader(handle))
            write_csv(path, data[:-1])
            with self.assertRaisesRegex(ValueError, 'coverage'):
                plots.load_run('filter', directory)
            # Evaluation-only plots can still use exports without intervention rows.
            self.assertEqual(len(plots.load_run('filter', directory, load_edits=False).points), 3)
            data[-1]['dpco_edited_count'] = '9'
            write_csv(path, data)
            with self.assertRaisesRegex(ValueError, 'invalid dpco_edited_count'):
                plots.load_run('filter', directory)

    def test_real_cpu_render_provenance_dimensions_and_styles(self):
        try:
            import matplotlib
            matplotlib.use('Agg')
            import matplotlib.pyplot as plt
            from PIL import Image
        except ImportError:
            self.skipTest('matplotlib / Pillow unavailable')
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            inputs, runs = all_fixtures(root)
            captured = []
            subplots = plt.subplots
            def capture(*args, **kwargs):
                fig, axes = subplots(*args, **kwargs)
                captured.append((fig, axes))
                return fig, axes
            with patch.object(plots, 'ROOT', root), patch.object(plt, 'subplots', side_effect=capture):
                output = plots.main(inputs + ['--output-name', 'verified', '--dpi', '70',
                    '--eval-smooth-window', '2', '--smooth-window', '2', '--edit-stride', '3',
                    '--tradeoff-trajectories', '--mark-steps', '2'])
                with self.assertRaises(SystemExit), patch('sys.stderr', StringIO()):
                    plots.main(inputs + ['--output-name', 'verified'])
            self.assertEqual(output, root / 'results/figure/verified')
            self.assertEqual(len(list(output.glob('*.png'))), 4)
            self.assertEqual(len(list(output.glob('*.pdf'))), 4)
            for image_path in output.glob('*.png'):
                with Image.open(image_path) as img:
                    self.assertEqual(img.size, (350, 280))
            manifest = json.loads((output / 'plot_manifest.json').read_text())
            self.assertEqual(manifest['status'], 'complete')
            self.assertEqual(len(manifest['sources']), 40)
            self.assertEqual(manifest['figure_inches'], [5, 4.])
            with (output / 'endpoints.csv').open() as handle:
                endpoints = list(csv.DictReader(handle))
            self.assertEqual(len(endpoints), 14)
            self.assertAlmostEqual(float(endpoints[0]['original_accuracy']), 20.)
            with (output / 'evaluation_curves.csv').open() as handle:
                evaluated = list(csv.DictReader(handle))
            self.assertAlmostEqual(float(evaluated[2]['smooth_original_accuracy']), 25.)
            with (output / 'edited_curves.csv').open() as handle:
                edits = list(csv.DictReader(handle))
            self.assertEqual([int(row['step']) for row in edits[:2]], [1, 4])
            self.assertEqual(float(edits[1]['smooth_edited_percent']), 43.75)
            for _, axes in captured:
                for ax in axes.flat:
                    for line in ax.lines:
                        if line.get_color() == '#ff7f0e':
                            self.assertEqual(line.get_linestyle(), '--')
                        elif line.get_color() in ('#1f77b4', '#d62728'):
                            self.assertEqual(line.get_linestyle(), '-')
            # The loader's source hashes still describe the untouched fixtures.
            import hashlib
            for run in runs:
                for path, sha in run.sources.items():
                    self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(), sha)


if __name__ == '__main__':
    unittest.main()
