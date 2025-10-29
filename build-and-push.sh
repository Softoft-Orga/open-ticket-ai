#!/bin/bash
set -euo pipefail

REPO=${REPO:-softotobo/open-ticket-ai}
VERSION=${VERSION:-}
PACKAGE_INDEX_URL=${PACKAGE_INDEX_URL:-https://pypi.org/simple}
PACKAGE_EXTRA_INDEX_URL=${PACKAGE_EXTRA_INDEX_URL:-}

if [[ -z "${VERSION}" ]]; then
  VERSION=$(uv run --with setuptools-scm python scripts/resolve_version.py)
fi

if [[ "${VERSION}" == *dev* ]]; then
  FLOATING_TAG=${FLOATING_TAG:-next}
else
  FLOATING_TAG=${FLOATING_TAG:-latest}
fi

echo "🔨 Building ${REPO}:${VERSION}..."

docker build \
  --build-arg PACKAGE_VERSION="${VERSION}" \
  --build-arg PACKAGE_INDEX_URL="${PACKAGE_INDEX_URL}" \
  --build-arg PACKAGE_EXTRA_INDEX_URL="${PACKAGE_EXTRA_INDEX_URL}" \
  -t "${REPO}:${VERSION}" \
  -t "${REPO}:${FLOATING_TAG}" \
  .

echo "🚀 Pushing to Docker Hub..."
docker push "${REPO}:${VERSION}"
docker push "${REPO}:${FLOATING_TAG}"

echo "✅ Done! Images pushed:"
echo "  - ${REPO}:${VERSION}"
echo "  - ${REPO}:${FLOATING_TAG}"
echo ""
echo "📦 Repository: https://hub.docker.com/r/${REPO}"
