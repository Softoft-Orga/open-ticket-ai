#!/usr/bin/env bash
set -euo pipefail

uv version --bump patch
uv build
uv publish

uv version --bump patch
uv build --package otai_hf_local
uv publish

uv version --bump patch
uv build --package otai_otobo_znuny
uv publish
