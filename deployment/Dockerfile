# syntax=docker/dockerfile:1.7
FROM python:3.14-slim-bookworm

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

RUN --mount=type=cache,target=/var/cache/apt \
    apt-get update && \
    apt-get install -y --no-install-recommends git ca-certificates && \
    rm -rf /var/lib/apt/lists/*

# upgrade pip first, then install your packages
RUN --mount=type=cache,target=/root/.cache/pip \
    pip install --upgrade pip && \
    pip install \
      open-ticket-ai \
      otai-base \
      otai-hf-local \
      otai-otobo-znuny

RUN useradd -m -u 10001 app && chown -R app:app /app
USER app

HEALTHCHECK --interval=30s --timeout=5s --retries=3 CMD python -c "import open_ticket_ai; print('ok')"
CMD ["python","-m","open_ticket_ai.main"]
