FROM ghcr.io/astral-sh/uv:python3.13-bookworm
SHELL ["/bin/bash", "-eo", "pipefail", "-c"]
WORKDIR /app

ARG PACKAGES
ARG VERSION
RUN test -n "$PACKAGES" && test -n "$VERSION"

# Minimal project so uv add has a place to write
RUN printf '[project]\nname="runtime"\nversion="0.0.0"\nrequires-python=">=3.13"\n' > pyproject.toml

# Add all packages at the same version, this both updates pyproject + installs
RUN for p in $PACKAGES; do uv add "$p==$VERSION"; done

# Optional: ensure environment fully synced (usually not needed, uv add already syncs)
# RUN uv sync --frozen

CMD ["uv","run","python","-m","open_ticket_ai"]
