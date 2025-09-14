# Use the official Python 3.13 slim image
FROM python:3.13-slim

# Set the working directory in the container
WORKDIR /app

# Copy the entire project into the container
COPY ../../open_ticket_ai ./open_ticket_ai
COPY ../../pyproject.toml ./pyproject.toml

# Install uv and the project dependencies
RUN pip install uv
RUN uv pip install --system --no-cache-dir -r pyproject.toml

# Command to run your application
CMD ["python", "open_ticket_ai/src/main.py"]
