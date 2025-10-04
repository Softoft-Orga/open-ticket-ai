#!/usr/bin/env python3
"""Example script to run the Flow Editor API server.

This script demonstrates how to run the API with custom settings.
"""

import os
import sys
from pathlib import Path

# Add src to Python path
src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))

# Set config path if not already set
if "CONFIG_PATH" not in os.environ:
    config_path = src_path / "config.yml"
    if config_path.exists():
        os.environ["CONFIG_PATH"] = str(config_path)
        print(f"Using config file: {config_path}")
    else:
        print(f"Warning: Config file not found at {config_path}")
        print("You can set a custom path using the CONFIG_PATH environment variable")

try:
    import uvicorn
    from open_ticket_ai.tools.flow_editor_api.main import app
except ImportError as e:
    print("Error: Required dependencies not installed")
    print(f"Details: {e}")
    print("\nPlease install the required packages:")
    print("  pip install fastapi uvicorn pydantic pydantic-settings pyyaml")
    sys.exit(1)


def main():
    """Run the API server."""
    print("\n" + "=" * 60)
    print("Open Ticket AI - Flow Editor API Server")
    print("=" * 60)
    print("\nStarting server...")
    print("  Host: 0.0.0.0")
    print("  Port: 8000")
    print("  CORS: http://localhost:5173")
    print("\nEndpoints:")
    print("  GET  /health     - Health check")
    print("  GET  /config     - Get current configuration")
    print("  PUT  /config     - Update configuration")
    print("  POST /convert    - Convert YAML to Mermaid")
    print("\nAPI Documentation:")
    print("  http://localhost:8000/docs")
    print("\nPress Ctrl+C to stop the server")
    print("=" * 60 + "\n")
    
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_level="info",
    )


if __name__ == "__main__":
    main()
