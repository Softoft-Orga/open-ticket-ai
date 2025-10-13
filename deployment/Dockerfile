FROM ghcr.io/astral-sh/uv:python3.13-bookworm-slim

# Set the working directory
WORKDIR /app

# Copy only the files needed to install dependencies
COPY ../pyproject.toml ./

# Create a virtual environment and install dependencies into it
# We allow caching here to speed up rebuilds
RUN uv sync
RUN uv add otai-hf-local
RUN uv add otai-otobo-znuny

ENV PYTHONPATH="/app"


# Set the PATH to use the virtual environment's python and pip
ENV PATH="/app/.venv/bin:$PATH"

# Copy the application source code
COPY ../src ./open_ticket_ai

# Command to run your application
CMD ["uv", "run", "./src/open_ticket_ai/main.py"]
