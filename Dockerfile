FROM ghcr.io/astral-sh/uv:python3.14-bookworm
WORKDIR /app

RUN uv pip install --system open-ticket-ai otai-hf-local otai-otobo-znuny

CMD ["python", "-m", "open_ticket_ai.main"]

