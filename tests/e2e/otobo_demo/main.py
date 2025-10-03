import asyncio
from pathlib import Path

from dotenv import load_dotenv

from open_ticket_ai.core.config.config_models import load_config
from open_ticket_ai.main import OpenTicketAIApp
from open_ticket_ai.tools.mermaid_conversion.graph_builder import Graph
from open_ticket_ai.tools.mermaid_conversion.renderer import build_mermaid_diagram
from open_ticket_ai.tools.mermaid_conversion.traverse import Traverser

CONFIG_PATH = Path(__file__).parent / "config.yml"

def write_mermaid_to_markdown(diagram: str, output_path: Path) -> None:
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("```mermaid\n")
        f.write(diagram)
        f.write("\n```\n")
    print(f"Mermaid diagram written to {output_path}")


def generate_mermaid():
    config = load_config(CONFIG_PATH)
    print(config.model_dump_json(indent=2))
    trav = Traverser(Graph())
    graph = trav.build_pipelines_from_config(config.model_dump())
    print(graph)
    diagram = build_mermaid_diagram(graph.nodes, graph.edges, graph.root_subgraphs)
    with open(CONFIG_PATH.parent / "config.mmd", "w", encoding="utf-8") as f:
        f.write(diagram)
    print(f"Mermaid diagram written to {CONFIG_PATH.parent / 'config.mmd'})")

    # Optionally, write to a markdown file
    write_mermaid_to_markdown(diagram, CONFIG_PATH.parent / "config.md")


if __name__ == '__main__':
    generate_mermaid()
    #load_dotenv(override=True)
    #asyncio.run(OpenTicketAIApp(Path(__file__).parent / "config.yml").run())
