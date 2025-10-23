FROM ghcr.io/astral-sh/uv:python3.14-bookworm
WORKDIR /app

ARG PACKAGE_VERSION
ARG PACKAGE_INDEX_URL=https://pypi.org/simple
ARG PACKAGE_EXTRA_INDEX_URL=

RUN test -n "$PACKAGE_VERSION" \
    && if [ -n "$PACKAGE_EXTRA_INDEX_URL" ]; then \
         uv pip install --system \
           --index-url "$PACKAGE_INDEX_URL" \
           --extra-index-url "$PACKAGE_EXTRA_INDEX_URL" \
           open-ticket-ai=="$PACKAGE_VERSION" \
           otai-hf-local=="$PACKAGE_VERSION" \
           otai-otobo-znuny=="$PACKAGE_VERSION" \
           otai-base=="$PACKAGE_VERSION"; \
       else \
         uv pip install --system \
           --index-url "$PACKAGE_INDEX_URL" \
           open-ticket-ai=="$PACKAGE_VERSION" \
           otai-hf-local=="$PACKAGE_VERSION" \
           otai-otobo-znuny=="$PACKAGE_VERSION" \
           otai-base=="$PACKAGE_VERSION"; \
       fi

CMD ["python", "-m", "open_ticket_ai.main"]
