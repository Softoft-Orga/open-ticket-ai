#!/bin/bash
set -e

VERSION="1.1.2"
REPO="softotobo/open-ticket-ai"

echo "🔨 Building ${REPO}:${VERSION}..."

# Build with all tags
docker build \
  -t ${REPO}:${VERSION} \
  -t ${REPO}:1.1 \
  -t ${REPO}:1 \
  -t ${REPO}:latest \
  .

echo "🚀 Pushing to Docker Hub..."
docker push --all-tags ${REPO}

echo "✅ Done! Images pushed:"
echo "  - ${REPO}:${VERSION}"
echo "  - ${REPO}:1.1"
echo "  - ${REPO}:1"
echo "  - ${REPO}:latest"
echo ""
echo "📦 Repository: https://hub.docker.com/r/${REPO}"