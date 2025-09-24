FROM ghcr.io/astral-sh/uv:python3.13-bookworm-slim

# Set the working directory
WORKDIR /app

# Copy only the files needed to install dependencies
COPY pyproject.toml ./
COPY LICENSE ./
COPY README.md ./

# Create a virtual environment and install dependencies into it
# We allow caching here to speed up rebuilds
RUN uv sync

ENV PYTHONPATH="/app"


# Set the PATH to use the virtual environment's python and pip
ENV PATH="/app/.venv/bin:$PATH"

# Copy the application source code
COPY open_ticket_ai ./open_ticket_ai

# Command to run your application
CMD ["python", "-m", "open_ticket_ai.src.main"]
