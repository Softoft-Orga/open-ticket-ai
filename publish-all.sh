#!/usr/bin/env bash
set -euo pipefail

uv version --bump patch
uv build
uv publish

cd packages/otai_hf_local
uv version --bump patch
uv build --package otai_hf_local
uv publish
cd ../..

cd packages/otai_otobo_znuny
uv version --bump patch
uv build --package otai_otobo_znuny
uv publish

cd ../..