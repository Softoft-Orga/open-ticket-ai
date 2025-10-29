FROM ghcr.io/astral-sh/uv:python3.14-bookworm-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    UV_LINK_MODE=copy \
    DEBIAN_FRONTEND=noninteractive

WORKDIR /app

RUN --mount=type=cache,target=/var/cache/apt \
    apt-get update && \
    apt-get purge -y --auto-remove --allow-change-held-packages \
        libexpat1-dev libexpat1-dev:amd64 || true && \
    apt-get install -y --no-install-recommends libexpat1 && \
    apt-get install -y --only-upgrade libexpat1 && \
    rm -rf /var/lib/apt/lists/* /usr/share/doc/libexpat1-dev || true

RUN --mount=type=cache,id=uvcache,sharing=locked,target=/root/.cache/uv \
    uv pip install --system \
      open-ticket-ai \
      otai-base \
      otai-hf-local \
      otai-otobo-znuny

RUN useradd -m -u 10001 app && chown -R app:app /app
USER app

HEALTHCHECK --interval=30s --timeout=5s --retries=3 CMD python -c "import open_ticket_ai; print('ok')"
CMD ["uv", "run", "-m", "open_ticket_ai.main"]
