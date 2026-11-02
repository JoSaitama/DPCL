"""Prepare official CIFAR-100N or a reproducible controlled human-noise cache."""

import argparse
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--stage", choices=("plan", "download", "verify", "controlled"), default="plan")
    parser.add_argument("--output-dir", type=Path,
                        help="Cache directory; required for controlled, otherwise ../data/cifar100n")
    parser.add_argument("--source-dir", type=Path,
                        help="Original human cache for controlled; default ../data/cifar100n")
    parser.add_argument("--target-noise-percent", type=float,
                        help="Controlled global mismatch percentage, not a training-time assertion")
    parser.add_argument("--selection-seed", type=int,
                        help="Controlled human-error selection RNG seed; default 0")
    args = parser.parse_args(argv)
    if args.stage == "controlled":
        if args.output_dir is None or args.target_noise_percent is None:
            parser.error("controlled requires --output-dir and --target-noise-percent")
    elif any(value is not None for value in
             (args.source_dir, args.target_noise_percent, args.selection_seed)):
        parser.error("--source-dir, --target-noise-percent and --selection-seed require --stage controlled")
    from src.data.cifar100n_prepare import ASSETS, REVISION, prepare, verify_prepared
    output = (args.output_dir or ROOT.parent / "data/cifar100n").expanduser().resolve()
    if args.stage == "plan":
        print(json.dumps({"output_dir": str(output), "official_revision": REVISION,
            "sources": {name: {"url": item[0], item[1]: item[2]} for name, item in ASSETS.items()},
            "split_counts": {"train": 50000, "test": 10000},
            "noise_percent_semantics": "measured label mismatch; not a human noise generator",
            "controlled_stage": {"target_noise_percent": "retain a fixed global number of source human errors",
                                 "selection_seed": 0, "requires_separate_output_dir": True},
            "runtime_dependencies": "numpy; certifi optional; no JAX/Torch/TensorFlow"}, indent=2))
        return
    if args.stage == "controlled":
        from src.data.cifar100n_controlled import prepare_controlled
        source = args.source_dir or ROOT.parent / "data/cifar100n"
        manifest, digest = prepare_controlled(source, output,
            target_noise_percent=args.target_noise_percent,
            selection_seed=0 if args.selection_seed is None else args.selection_seed)
        print(json.dumps({"event": "controlled_human_ready", "output_dir": str(output),
                          "manifest_sha256": digest, **manifest}, indent=2))
        return
    manifest, digest = (prepare(output, download=True,
        progress=lambda **fields: print(json.dumps(fields), flush=True)) if args.stage == "download"
        else verify_prepared(output))
    print(json.dumps({"event": "verified", "output_dir": str(output),
                      "manifest_sha256": digest, **manifest}, indent=2))


if __name__ == "__main__":
    main()
