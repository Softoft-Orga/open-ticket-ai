FROM python:3.14-alpine

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

RUN apk add --no-cache expat ca-certificates git

RUN --mount=type=cache,target=/root/.cache/pip \
    apk add --no-cache --virtual .build-deps build-base rust cargo && \
    pip install \
      open-ticket-ai \
      otai-base \
      otai-hf-local \
      otai-otobo-znuny && \
    apk del .build-deps

RUN adduser -D -u 10001 app && chown -R app:app /app
USER app

HEALTHCHECK --interval=30s --timeout=5s --retries=3 CMD python -c "import open_ticket_ai; print('ok')"
CMD ["python","-m","open_ticket_ai.main"]