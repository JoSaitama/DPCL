"""Inspect, download or verify the pinned sklearn Digits source."""

import argparse
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--stage", choices=("plan", "download", "verify"), default="plan")
    parser.add_argument("--output-dir", type=Path, default=ROOT.parent / "data/digits")
    args = parser.parse_args()
    from src.data.digits import SOURCE_URL, SOURCE_SHA256, SAMPLE_COUNT, TEST_COUNT, SPLIT_SEED, DigitsImages
    root = args.output_dir.expanduser().resolve()
    if args.stage == "plan":
        print(json.dumps({"output_dir": str(root), "source_url": SOURCE_URL, "source_sha256": SOURCE_SHA256,
                          "train": SAMPLE_COUNT - TEST_COUNT, "test": TEST_COUNT, "split_seed": SPLIT_SEED}, indent=2))
        return
    data = DigitsImages(root, download=args.stage == "download",
                        progress=lambda **fields: print(json.dumps(fields), flush=True))
    print(json.dumps({"event": "digits_ready", "source_file": str(data.path), **data.identity}, indent=2))


if __name__ == "__main__":
    main()
