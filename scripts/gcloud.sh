#!/usr/bin/env sh
set -eu

SCRIPT_DIR="$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"

CLOUDSDK_CONFIG="${CLOUDSDK_CONFIG:-${PROJECT_DIR}/.gcloud-config}" \
  "${PROJECT_DIR}/tools/google-cloud-sdk/bin/gcloud" "$@"
