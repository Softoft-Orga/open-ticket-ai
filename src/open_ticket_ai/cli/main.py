import asyncio
import importlib.metadata
import os
import subprocess
from pathlib import Path

import typer
import yaml  # type: ignore[import-untyped]
from pydantic import ValidationError
from rich.console import Console

from open_ticket_ai import __version__
from open_ticket_ai.core.config.config_models import RawOpenTicketAIConfig
from open_ticket_ai.main import run

app = typer.Typer(help="Open Ticket AI CLI - Manage configurations and templates")
console = Console()


def get_templates_dir() -> Path:
    package_root = Path(__file__).parent.parent.parent.parent
    templates_dir = package_root / "docs" / "raw_en_docs" / "config_examples"
    return templates_dir


def get_available_templates() -> dict[str, Path]:
    templates_dir = get_templates_dir()

    if not templates_dir.exists():
        return {}

    templates = {}
    for yml_file in templates_dir.glob("*.yml"):
        if yml_file.stem not in ["AGENTS", "QUICK_REFERENCE", "README"]:
            templates[yml_file.stem] = yml_file

    return templates


def extract_template_description(template_path: Path) -> str:
    with open(template_path) as f:
        lines = f.readlines()
        description_lines = []
        for line in lines:
            if line.strip().startswith("#"):
                clean_line = line.strip().lstrip("#").strip()
                if clean_line and not clean_line.startswith("Example:"):
                    description_lines.append(clean_line)
                if clean_line.startswith("Example:"):
                    description_lines = [clean_line]
                    break
            else:
                break

        return " ".join(description_lines) if description_lines else "No description available"


@app.command()
def init(
    template: str = typer.Argument(..., help="Template name to initialize from"),
    output: Path = typer.Option("config.yml", "--output", "-o", help="Output file path"),
    force: bool = typer.Option(False, "--force", "-f", help="Overwrite existing file"),
) -> None:
    templates = get_available_templates()

    if template not in templates:
        console.print(f"[red]✗ Template '{template}' not found[/red]")
        console.print("\n[yellow]Available templates:[/yellow]")
        for tmpl_name in sorted(templates.keys()):
            console.print(f"  • {tmpl_name}")
        raise typer.Exit(1)

    if output.exists() and not force:
        console.print(f"[red]✗ File '{output}' already exists. Use --force to overwrite.[/red]")
        raise typer.Exit(1)

    template_path = templates[template]

    try:
        with open(template_path) as src:
            content = src.read()

        with open(output, "w") as dst:
            dst.write(content)

        console.print(f"[green]✅ Successfully initialized config from template '{template}'[/green]")
        console.print(f"   Created: {output}")
        console.print("\n[cyan]📝 Next steps:[/cyan]")
        console.print("   1. Edit config.yml to customize your configuration")
        console.print("   2. Update environment variables (server addresses, credentials)")
        console.print("   3. Validate with: otai check-config config.yml")
        console.print("   4. Start with: otai start --config config.yml")

    except Exception as e:
        console.print(f"[red]✗ Failed to initialize template: {e}[/red]")
        raise typer.Exit(1) from e


@app.command()
def start(
    config: Path | None = typer.Option(
        None,
        "--config",
        "-c",
        help="Path to config.yml file (uses OPEN_TICKET_AI_CONFIG env var if not provided)",
    ),
) -> None:
    config_path = config

    if config_path is None:
        env_config = os.getenv("OPEN_TICKET_AI_CONFIG")
        if env_config:
            config_path = Path(env_config)
        else:
            console.print("[red]❌ Error: OPEN_TICKET_AI_CONFIG environment variable not set[/red]")
            console.print("\nPlease either:")
            console.print("  1. Set the environment variable: export OPEN_TICKET_AI_CONFIG=/path/to/config.yml")
            console.print("  2. Use the --config option: otai start --config config.yml")
            raise typer.Exit(1)

    if not config_path.exists():
        console.print(f"[red]❌ Error: Config file not found: {config_path}[/red]")
        raise typer.Exit(1)

    console.print(f"[green]🚀 Starting Open Ticket AI with config: {config_path}[/green]")

    try:
        asyncio.run(run(str(config_path)))
    except KeyboardInterrupt:
        console.print("\n[yellow]⚠ Shutting down...[/yellow]")
    except Exception as e:
        console.print(f"[red]❌ Error: {e}[/red]")
        raise typer.Exit(1) from e


@app.command(name="check-config")
def check_config(
    config_path: Path = typer.Argument("config.yml", help="Path to config.yml file to validate"),
) -> None:
    if not config_path.exists():
        console.print(f"[red]❌ Error: Config file not found: {config_path}[/red]")
        raise typer.Exit(1)

    console.print(f"[cyan]🔍 Validating config file: {config_path}[/cyan]")

    try:
        with open(config_path) as f:
            raw_config = yaml.safe_load(f)

        config = RawOpenTicketAIConfig.model_validate(raw_config.get("open_ticket_ai", {}))

        num_plugins = len(config.plugins) if config.plugins else 0
        num_defs = len(config.defs) if config.defs else 0
        num_orchestrator = len(config.orchestrator.runners) if config.orchestrator else 0

        console.print("[green]✅ Config file is valid![/green]")
        console.print(f"   - Plugins: {num_plugins}")
        console.print(f"   - Definitions: {num_defs}")
        console.print(f"   - Orchestrator steps: {num_orchestrator}")

    except ValidationError as e:
        console.print("[red]❌ Config validation failed:[/red]\n")
        for error in e.errors():
            location = " -> ".join(str(loc) for loc in error["loc"])
            console.print(f"  [yellow]{location}:[/yellow] {error['msg']}")
        raise typer.Exit(1) from e
    except yaml.YAMLError as e:
        console.print(f"[red]❌ YAML parsing error: {e}[/red]")
        raise typer.Exit(1) from e
    except Exception as e:
        console.print(f"[red]❌ Error: {e}[/red]")
        raise typer.Exit(1) from e


@app.command()
def version() -> None:
    console.print(f"Open Ticket AI version: {__version__}")


plugin_app = typer.Typer(help="Manage OTAI plugins")
app.add_typer(plugin_app, name="plugin")


@plugin_app.command("list")
def plugin_list() -> None:
    console.print("[cyan]📦 Installed OTAI plugins:[/cyan]\n")

    found_plugins = False
    for dist in importlib.metadata.distributions():
        if dist.name.startswith("otai-") or "open-ticket-ai" in dist.name:
            found_plugins = True
            version = dist.version
            metadata = dist.metadata
            description = metadata.get("Summary", "No description")

            console.print(f"  • [bold]{dist.name}[/bold] (v{version})")
            console.print(f"    {description}")
            console.print()

    if not found_plugins:
        console.print("  [yellow]No OTAI plugins found[/yellow]")


@plugin_app.command("install")
def plugin_install(
    package_name: str = typer.Argument(..., help="Plugin package name to install"),
    upgrade: bool = typer.Option(False, "--upgrade", "-U", help="Upgrade if already installed"),
) -> None:
    console.print(f"[cyan]📥 Installing plugin: {package_name}[/cyan]")

    cmd = ["pip", "install", package_name]
    if upgrade:
        cmd.append("--upgrade")

    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        console.print(f"[green]✅ Successfully installed {package_name}[/green]")
        if result.stdout:
            console.print(result.stdout)
    except subprocess.CalledProcessError as e:
        console.print(f"[red]❌ Failed to install plugin: {e}[/red]")
        if e.stderr:
            console.print(e.stderr)
        raise typer.Exit(1) from e


@plugin_app.command("remove")
def plugin_remove(
    package_name: str = typer.Argument(..., help="Plugin package name to remove"),
    yes: bool = typer.Option(False, "--yes", "-y", help="Skip confirmation prompt"),
) -> None:
    if not yes:
        confirm = typer.confirm(f"Are you sure you want to remove {package_name}?")
        if not confirm:
            console.print("[yellow]Cancelled[/yellow]")
            raise typer.Exit(0)

    console.print(f"[cyan]🗑️  Removing plugin: {package_name}[/cyan]")

    try:
        subprocess.run(["pip", "uninstall", "-y", package_name], check=True, capture_output=True)
        console.print(f"[green]✅ Successfully removed {package_name}[/green]")
    except subprocess.CalledProcessError as e:
        console.print(f"[red]❌ Failed to remove plugin: {e}[/red]")
        raise typer.Exit(1) from e


@app.command()
def upgrade(
    check_only: bool = typer.Option(False, "--check-only", help="Only check for updates, don't install"),
) -> None:
    package_name = "open-ticket-ai"

    if check_only:
        console.print(f"[cyan]🔍 Checking for updates to {package_name}...[/cyan]")
        try:
            result = subprocess.run(
                ["pip", "index", "versions", package_name],
                check=True,
                capture_output=True,
                text=True,
            )
            console.print(result.stdout)
        except subprocess.CalledProcessError:
            console.print("[yellow]Could not check for updates[/yellow]")
    else:
        console.print(f"[cyan]⬆️  Upgrading {package_name}...[/cyan]")
        try:
            subprocess.run(
                ["pip", "install", "--upgrade", package_name],
                check=True,
            )
            console.print(f"[green]✅ Successfully upgraded {package_name}[/green]")
        except subprocess.CalledProcessError as e:
            console.print(f"[red]❌ Failed to upgrade: {e}[/red]")
            raise typer.Exit(1) from e


def main() -> None:
    app()


if __name__ == "__main__":
    main()
