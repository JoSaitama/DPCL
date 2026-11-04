#!/usr/bin/env bash
# Shared sequential coordinator; fixed author Red split for all three methods.
set -euo pipefail
suite_root="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
exec bash "$suite_root/run_dpcl_suite.sh" \
  --config configs/tpu/cnwl/dpcl_adam.toml \
  --methods adam dpcl_filter dpcl_flip "$@"
