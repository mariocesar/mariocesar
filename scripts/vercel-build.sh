#!/usr/bin/env bash
set -euo pipefail

export PATH="$HOME/.local/bin:$PATH"
export UV_CACHE_DIR="${UV_CACHE_DIR:-/tmp/uv-cache}"

if ! command -v uv >/dev/null 2>&1; then
    python3 -m pip install --user uv
fi

uv run --frozen python -m builder.build
