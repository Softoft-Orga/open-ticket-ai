"""Business logic for YAML configuration and Mermaid diagram conversion."""

from pathlib import Path

from open_ticket_ai.diagram import ConfigFlowDiagramGenerator
from .storage import read_text_file, write_text_file


def load_config_yaml(config_path: Path) -> str:
    """Load configuration YAML from file.

    Args:
        config_path: Path to the configuration file

    Returns:
        Configuration content as YAML string

    Raises:
        FileNotFoundError: If the config file doesn't exist
    """
    return read_text_file(config_path)


def save_config_yaml(config_path: Path, yaml_content: str) -> None:
    """Save configuration YAML to file.

    Args:
        config_path: Path to the configuration file
        yaml_content: YAML content to save

    Raises:
        IOError: If writing fails
    """
    write_text_file(config_path, yaml_content)


def convert_yaml_to_mermaid(
    yaml_content: str | None,
    config_path: Path,
    direction: str = "TD",
    wrap: bool = False
) -> str:
    """Convert YAML configuration to Mermaid diagram.

    Args:
        yaml_content: Optional YAML content to convert. If None, reads from config_path
        config_path: Path to the configuration file (used when yaml_content is None)
        direction: Mermaid diagram direction (TD for top-down, LR for left-right)
        wrap: Whether to wrap long labels (currently not implemented in renderer)

    Returns:
        Mermaid diagram as string

    Raises:
        ValueError: If YAML is invalid or config is malformed
        FileNotFoundError: If config_path doesn't exist when yaml_content is None
    """
    # If YAML content is provided, write it to a temporary location
    if yaml_content is not None:
        # Create a temporary file to pass to the generator
        import tempfile
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yml', delete=False, encoding='utf-8') as tmp:
            tmp.write(yaml_content)
            tmp_path = Path(tmp.name)

        try:
            generator = ConfigFlowDiagramGenerator(tmp_path)
            diagrams = generator.generate()
        finally:
            # Clean up temporary file
            tmp_path.unlink(missing_ok=True)
    else:
        # Use the provided config path
        generator = ConfigFlowDiagramGenerator(config_path)
        diagrams = generator.generate()

    # If direction is LR, we need to modify the diagrams
    if direction == "LR":
        diagrams = {
            name: diagram.replace("flowchart TD", "flowchart LR", 1)
            for name, diagram in diagrams.items()
        }

    # Combine all diagrams into one output
    if not diagrams:
        return "flowchart TD\n    Start[No pipelines found]"

    # Return the first diagram (or combine multiple if needed)
    # For MVP, we'll just return all diagrams separated
    result = []
    for name, diagram in diagrams.items():
        result.append(f"--- {name} ---\n{diagram}")

    return "\n\n".join(result)
