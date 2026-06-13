#!/usr/bin/env sh
set -eu

SCRIPT_DIR="$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"

"${PROJECT_DIR}/tools/gh_2.94.0_macOS_arm64/bin/gh" "$@"
