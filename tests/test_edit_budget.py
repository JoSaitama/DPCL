"""Budget rounding, launch contracts, and capped gradient selection."""

from dataclasses import replace
import json
from pathlib import Path
import subprocess
import sys
from tempfile import TemporaryDirectory
import unittest

from src.config import load_config
from src.edit_budget import percent_caps, validate_edit_budget
from src.training.launch import resolve_config

ROOT = Path(__file__).resolve().parents[1]
CONFIG = ROOT / "configs/tpu/digits/dpcl_adam.toml"


class EditBudgetTests(unittest.TestCase):
    def test_decimal_ceil_and_validation(self):
        self.assertEqual(percent_caps(256, 10)[256], 26)
        self.assertEqual(percent_caps(100, 7)[100], 7)
        self.assertEqual(percent_caps(8, 12.5), [0] + [1] * 8)
        for k, pct in ((-1, None), (True, None), (2, 10), (None, -1), (None, 101), (None, float("nan"))):
            with self.assertRaises(ValueError):
                validate_edit_budget(k, pct)

    def test_suite_baseline_and_effective_caps(self):
        cmd = [sys.executable, str(ROOT / "scripts/run_suite.py"), "--config", str(CONFIG),
            "--methods", "adam", "dpcl_flip", "dpcl_filter", "self_flip", "self_filter", "--dry-run"]
        for flag, option, value, suffix in (
                ("--bottom-k", "bottom_k", 6, "_k6_"),
                ("--bottom-k-percent", "bottom_k_percent", 10, "_kpct10_")):
            plans = json.loads(subprocess.check_output([*cmd, flag, str(value)], text=True))
            self.assertEqual([p[option] for p in plans], [None, value, value, value, value])
            self.assertNotIn(suffix, plans[0]["stdout"])
            self.assertTrue(all(suffix in p["stdout"] for p in plans[1:]))
            for name, plan in zip(("adam", "dpcl_flip", "dpcl_filter", "self_flip", "self_filter"), plans):
                child = plan["command"]
                self.assertEqual(child[child.index(flag) + 1], str(value) if flag == "--bottom-k" else "10.0")
                cfg = resolve_config(CONFIG, mode="train", method=name, **{option: value})
                self.assertEqual(getattr(cfg.method, option), plan[option])
        bad = subprocess.run([*cmd, "--bottom-k", "6", "--bottom-k-percent", "10"], capture_output=True, text=True)
        self.assertNotEqual(bad.returncode, 0)

    def test_toml_budget_is_retained_or_explicitly_overridden(self):
        with TemporaryDirectory() as tmp:
            path = Path(tmp) / "preset.toml"
            path.write_text(CONFIG.read_text().replace("negative_weight = -1.0", "negative_weight = -1.0\nbottom_k = 6"))
            self.assertEqual(resolve_config(path, mode="train", method="self_flip").method.bottom_k, 6)
            c = resolve_config(path, mode="train", method="dpcl_filter", bottom_k_percent=10)
            self.assertIsNone(c.method.bottom_k)
            self.assertEqual(c.method.bottom_k_percent, 10)
        c = load_config(CONFIG)
        with self.assertRaisesRegex(ValueError, "require dpcl with EMA"):
            replace(c, reference=replace(c.reference, name="loss"),
                    method=replace(c.method, bottom_k=6)).validate()

    def test_jitted_selection_and_gradient_keep_global_batch_denominator(self):
        try:
            import jax
            import jax.numpy as jnp
        except ModuleNotFoundError:
            self.skipTest("JAX is not installed")
        import numpy as np
        from src.methods.dpcl_history import HistoricalDPCL
        from tests.helpers import QuadraticTask

        scores = jnp.array([-2., -3., -3., -.5, 0., 2., -99., 1.])
        valid = jnp.array([1, 1, 1, 1, 1, 1, 0, 1], dtype=bool)
        negative = valid & (scores < 0)
        for kwargs, ids in (({}, [0, 1, 2, 3]), ({"bottom_k": 1}, [1]),
                            ({"bottom_k": 30}, [0, 1, 2, 3]), ({"bottom_k": 0}, []),
                            ({"bottom_k_percent": 40}, [0, 1, 2]),
                            ({"bottom_k_percent": 12.5}, [1])):
            with self.subTest(kwargs=kwargs):
                selector = jax.jit(HistoricalDPCL(**kwargs).select_edits)
                np.testing.assert_array_equal(np.flatnonzero(selector(scores, valid, negative)), ids)

        gradients = jnp.array([8., -1., -3., -3., 4., 0., -99.])
        mask = jnp.array([1, 1, 1, 1, 1, 1, 0], dtype=bool)
        batch = (-gradients[:, None], mask, jnp.zeros_like(mask))
        for backend in ("audit", "jvp"):
            for weight, expected in ((0., 8. / 6), (-1., 11. / 6)):
                method = HistoricalDPCL(0., weight, backend, bottom_k=1)
                result = jax.jit(lambda p: method.compute_direction(QuadraticTask(), p, batch))(
                    {"x": jnp.zeros(1)})
                np.testing.assert_allclose(result.direction["x"], [expected], atol=1e-6)
                np.testing.assert_allclose(result.method_state.mean["x"], [5. / 6], atol=1e-6)
                self.assertEqual(int(result.metrics["dpcl_negative_count"]), 3)
                self.assertEqual(int(result.metrics["dpcl_edited_count"]), 1)
