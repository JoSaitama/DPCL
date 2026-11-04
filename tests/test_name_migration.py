"""New launch contracts and read-only compatibility with historical exports."""

import json
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from src.config import load_config
from src.training.launch import resolve_config
from tests.test_noise_training_plots import fixture as noise_fixture, plots as noise_plots
from tests.test_dpcl_evaluation_plots import fixture as eval_fixture, plots as eval_plots
from scripts.plot_training_results import method_identity


ROOT = Path(__file__).resolve().parents[1]


class NameMigrationTests(unittest.TestCase):
    def test_every_preset_and_new_method_contract(self):
        for path in (ROOT / 'configs').rglob('*.toml'):
            with self.subTest(path=path):
                self.assertNotIn('dpco', path.as_posix())
                config = load_config(path)
                self.assertNotIn('dpco', config.method.name)
        path = ROOT / 'configs/tpu/cifar100n/dpcl_adam.toml'
        for name, weight in (('dpcl_flip', -1), ('dpcl_filter', 0)):
            config = resolve_config(path, mode='train', method=name)
            self.assertEqual(config.method.name, 'dpcl')
            self.assertEqual(config.method.negative_weight, weight)
            self.assertEqual(config.reference.name, 'ema')
            self.assertEqual(config.training.optimizer, 'adam')

    def test_old_edit_columns_metadata_and_run_name_remain_readable(self):
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            directory = noise_fixture(root, 'flip', .96)
            renamed = directory.with_name(directory.name.replace('dpcl', 'dpco'))
            directory.rename(renamed)
            source = renamed / 'dpcl_steps.csv'
            legacy = renamed / 'dpco_steps.csv'
            legacy.write_bytes(source.read_bytes().replace(b'dpcl_', b'dpco_'))
            source.unlink()
            logs = root / 'logs' / renamed.name
            logs.mkdir(parents=True)
            metadata = logs / 'metadata.json'
            metadata.write_text(json.dumps({'config': {'seed': 42,
                'training': {'optimizer': 'adam'},
                'method': {'name': 'dpco', 'negative_weight': -1},
                'reference': {'name': 'ema', 'beta': .96}}}))
            before = {p: p.read_bytes() for p in (*renamed.iterdir(), metadata)}
            run = noise_plots.load_run('flip', renamed)
            self.assertEqual(len(run.edits), 4)
            self.assertIn(legacy.resolve(), run.sources)
            self.assertEqual(run.metadata['config']['method']['name'], 'dpco')
            with self.assertRaisesRegex(ValueError, 'Adam baseline'):
                noise_plots.load_run('adam', renamed)
            self.assertTrue(all(p.read_bytes() == data for p, data in before.items()))

    def test_old_sgd_seed_and_adam_metadata_read_only(self):
        path = Path('mnist_noisy_mnist_cnn_dpco_ema_b0.9_w-1_43_0.001')
        self.assertEqual(eval_plots.directory_identity(path), (None, 43))
        with TemporaryDirectory() as tmp:
            directory = Path(tmp) / 'results/files/legacy_adam_42'
            eval_fixture(directory, seed=42, method='flip')
            metadata = directory.parent.parent / 'logs' / directory.name / 'metadata.json'
            data = metadata.read_bytes().replace(b'"dpcl"', b'"dpco"')
            metadata.write_bytes(data)
            run = eval_plots.load_evaluation_run('flip', directory, optimizer='adam')
            self.assertEqual(run.metadata['config']['method']['name'], 'dpco')
            self.assertEqual(metadata.read_bytes(), data)

    def test_legacy_policy_identity_uses_new_display_name(self):
        config = {'training': {'optimizer': 'sgd'},
                  'method': {'name': 'dpco_policy', 'policy_mode': 'alternating',
                             'alternating_first': 'dpco'},
                  'reference': {'name': 'error'}}
        before = json.dumps(config)
        self.assertEqual(method_identity(config), ('DPCL-E', 'alternating', 'dpcl'))
        config['method']['dpco_warmup_percent'] = 10
        self.assertEqual(method_identity(config), ('DPCL-E', 'warmup10', None))
        del config['method']['dpco_warmup_percent']
        self.assertEqual(json.dumps(config), before)
