FROM ghcr.io/astral-sh/uv:python3.14-bookworm
WORKDIR /app

uv add open-ticket-ai otai-hf-local otai-otobo-znuny

CMD ["uv","run", "open_ticket_ai.main"]

