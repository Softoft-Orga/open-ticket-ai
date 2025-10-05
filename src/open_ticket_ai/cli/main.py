import asyncio
import importlib.metadata as md
import os
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Annotated

import typer
from pydantic import ValidationError

from open_ticket_ai.core.config.config_models import load_config

app = typer.Typer(
    name="otai",
    help="Open Ticket AI - CLI utility for OTAI core features",
    add_completion=False,
)

plugin_app = typer.Typer(help="Manage OTAI plugins")
app.add_typer(plugin_app, name="plugin")

CONFIG_EXAMPLES = {
    "add_note": "add_note_when_in_queue.yml",
    "create_ticket": "create_ticket_on_condition.yml",
    "queue_classification": "queue_classification.yml",
    "priority_classification": "priority_classification.yml",
    "complete_workflow": "complete_workflow.yml",
}


def get_config_examples_dir() -> Path:
    try:
        package_path = Path(md.distribution("open-ticket-ai").locate_file(""))
        config_examples_path = package_path.parent.parent.parent / "docs" / "config_examples"
        if config_examples_path.exists():
            return config_examples_path
    except Exception:
        pass
    
    current_file = Path(__file__).resolve()
    repo_root = current_file.parent.parent.parent.parent
    config_examples_path = repo_root / "docs" / "config_examples"
    
    if config_examples_path.exists():
        return config_examples_path
    
    return Path("docs/config_examples")


@app.command()
def start(
    config: Annotated[
        str | None,
        typer.Option("--config", "-c", help="Path to config.yml file"),
    ] = None,
):
    if config:
        os.environ["OPEN_TICKET_AI_CONFIG"] = config
    
    config_path = os.getenv("OPEN_TICKET_AI_CONFIG")
    if not config_path:
        typer.echo("❌ Error: OPEN_TICKET_AI_CONFIG environment variable not set", err=True)
        typer.echo("   Set it or use --config option to specify config file", err=True)
        raise typer.Exit(1)
    
    if not Path(config_path).exists():
        typer.echo(f"❌ Error: Config file not found: {config_path}", err=True)
        raise typer.Exit(1)
    
    typer.echo(f"🚀 Starting Open Ticket AI with config: {config_path}")
    
    from open_ticket_ai.main import run  # noqa: PLC0415
    
    try:
        asyncio.run(run())
    except KeyboardInterrupt:
        typer.echo("\n⚠️  Shutdown requested...")
    except Exception as e:
        typer.echo(f"❌ Error: {e}", err=True)
        raise typer.Exit(1) from e


@app.command()
def check_config(
    config: Annotated[
        str,
        typer.Argument(help="Path to config.yml file to validate"),
    ] = "config.yml",
):
    config_path = Path(config)
    
    if not config_path.exists():
        typer.echo(f"❌ Error: Config file not found: {config_path}", err=True)
        raise typer.Exit(1)
    
    typer.echo(f"🔍 Validating config file: {config_path}")
    
    try:
        cfg = load_config(config_path)
        typer.echo("✅ Config file is valid!")
        typer.echo(f"   - Plugins: {len(cfg.plugins)}")
        typer.echo(f"   - Definitions: {len(cfg.defs)}")
        typer.echo(f"   - Orchestrator steps: {len(cfg.orchestrator)}")
        
        if cfg.plugins:
            typer.echo(f"   - Plugin list: {', '.join(cfg.plugins)}")
            
    except ValidationError as e:
        typer.echo("❌ Config validation failed:", err=True)
        for error in e.errors():
            loc = " -> ".join(str(x) for x in error["loc"])
            typer.echo(f"   {loc}: {error['msg']}", err=True)
        raise typer.Exit(1) from e
    except ValueError as e:
        typer.echo(f"❌ Config validation failed: {e}", err=True)
        raise typer.Exit(1) from e
    except Exception as e:
        typer.echo(f"❌ Unexpected error: {e}", err=True)
        raise typer.Exit(1) from e


@app.command()
def init(
    template: Annotated[
        str,
        typer.Argument(help="Template name to initialize from"),
    ],
    output: Annotated[
        str,
        typer.Option("--output", "-o", help="Output file path"),
    ] = "config.yml",
    force: Annotated[
        bool,
        typer.Option("--force", "-f", help="Overwrite existing file"),
    ] = False,
):
    output_path = Path(output)
    
    if output_path.exists() and not force:
        typer.echo(f"❌ Error: File already exists: {output_path}", err=True)
        typer.echo("   Use --force to overwrite", err=True)
        raise typer.Exit(1)
    
    if template not in CONFIG_EXAMPLES:
        typer.echo(f"❌ Error: Unknown template: {template}", err=True)
        typer.echo(f"   Available templates: {', '.join(CONFIG_EXAMPLES.keys())}", err=True)
        raise typer.Exit(1)
    
    config_examples_dir = get_config_examples_dir()
    template_file = config_examples_dir / CONFIG_EXAMPLES[template]
    
    if not template_file.exists():
        typer.echo(f"❌ Error: Template file not found: {template_file}", err=True)
        typer.echo("   Make sure the open-ticket-ai package is properly installed", err=True)
        raise typer.Exit(1)
    
    try:
        shutil.copy(template_file, output_path)
        typer.echo(f"✅ Successfully initialized config from template '{template}'")
        typer.echo(f"   Created: {output_path}")
        typer.echo("\n📝 Next steps:")
        typer.echo(f"   1. Edit {output_path} to customize your configuration")
        typer.echo("   2. Update environment variables (server addresses, credentials)")
        typer.echo(f"   3. Validate with: otai check-config {output_path}")
        typer.echo(f"   4. Start with: otai start --config {output_path}")
    except Exception as e:
        typer.echo(f"❌ Error copying template: {e}", err=True)
        raise typer.Exit(1) from e


@plugin_app.command("list")
def plugin_list():
    typer.echo("📦 Installed OTAI plugins:\n")
    
    found_any = False
    for ep in md.entry_points(group="open_ticket_ai.plugins"):
        found_any = True
        try:
            plugin = ep.load()
            meta = getattr(plugin, "get_metadata", lambda: {})()
            
            name = meta.get("name", ep.name)
            version = meta.get("version", "unknown")
            core_api = meta.get("core_api", "unknown")
            description = meta.get("description", "No description")
            
            typer.echo(f"  • {name} (v{version})")
            typer.echo(f"    {description}")
            typer.echo(f"    Core API: {core_api}")
            typer.echo()
        except Exception as e:
            typer.echo(f"  • {ep.name} (failed to load: {e})")
            typer.echo()
    
    if not found_any:
        typer.echo("  No plugins installed")
        typer.echo("\n💡 Install plugins with: otai plugin install <name>")


@plugin_app.command("install")
def plugin_install(
    name: Annotated[
        str,
        typer.Argument(help="Plugin package name to install"),
    ],
    upgrade: Annotated[
        bool,
        typer.Option("--upgrade", "-U", help="Upgrade if already installed"),
    ] = False,
):
    typer.echo(f"📦 Installing plugin: {name}")
    
    cmd = [sys.executable, "-m", "pip", "install"]
    if upgrade:
        cmd.append("--upgrade")
    cmd.append(name)
    
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        typer.echo(result.stdout)
        typer.echo(f"✅ Successfully installed {name}")
        typer.echo("\n💡 Run 'otai plugin list' to see all installed plugins")
    except subprocess.CalledProcessError as e:
        typer.echo(f"❌ Failed to install {name}:", err=True)
        typer.echo(e.stderr, err=True)
        raise typer.Exit(1) from e


@plugin_app.command("remove")
def plugin_remove(
    name: Annotated[
        str,
        typer.Argument(help="Plugin package name to remove"),
    ],
    yes: Annotated[
        bool,
        typer.Option("--yes", "-y", help="Skip confirmation"),
    ] = False,
):
    if not yes:
        confirm = typer.confirm(f"Are you sure you want to remove '{name}'?")
        if not confirm:
            typer.echo("❌ Cancelled")
            raise typer.Exit(0)
    
    typer.echo(f"🗑️  Removing plugin: {name}")
    
    cmd = [sys.executable, "-m", "pip", "uninstall", "-y", name]
    
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        typer.echo(result.stdout)
        typer.echo(f"✅ Successfully removed {name}")
    except subprocess.CalledProcessError as e:
        typer.echo(f"❌ Failed to remove {name}:", err=True)
        typer.echo(e.stderr, err=True)
        raise typer.Exit(1) from e


@app.command()
def upgrade(
    check_only: Annotated[
        bool,
        typer.Option("--check-only", help="Only check for updates, don't install"),
    ] = False,
):
    package_name = "open-ticket-ai"
    
    try:
        current_version = md.version(package_name)
        typer.echo(f"📦 Current version: {current_version}")
    except Exception as e:
        typer.echo(f"❌ Error: Could not determine current version of {package_name}", err=True)
        raise typer.Exit(1) from e
    
    typer.echo("🔍 Checking for updates...")
    
    try:
        result = subprocess.run(
            [sys.executable, "-m", "pip", "index", "versions", package_name],
            check=True,
            capture_output=True,
            text=True,
        )
        
        typer.echo("Available versions from PyPI:")
        typer.echo(result.stdout)
        
        if check_only:
            typer.echo("\n💡 To upgrade, run: otai upgrade")
            return
        
        confirm = typer.confirm("Do you want to upgrade to the latest version?")
        if not confirm:
            typer.echo("❌ Cancelled")
            raise typer.Exit(0)
        
        typer.echo("⬆️  Upgrading...")
        upgrade_result = subprocess.run(
            [sys.executable, "-m", "pip", "install", "--upgrade", package_name],
            check=True,
            capture_output=True,
            text=True,
        )
        typer.echo(upgrade_result.stdout)
        
        new_version = md.version(package_name)
        if new_version != current_version:
            typer.echo(f"✅ Successfully upgraded from {current_version} to {new_version}")
        else:
            typer.echo(f"✅ Already at latest version: {current_version}")
            
    except subprocess.CalledProcessError as e:
        typer.echo(f"❌ Error checking/upgrading: {e}", err=True)
        if e.stderr:
            typer.echo(e.stderr, err=True)
        raise typer.Exit(1) from e


@app.command()
def version():
    try:
        version = md.version("open-ticket-ai")
        typer.echo(f"Open Ticket AI version: {version}")
    except Exception:
        typer.echo("Open Ticket AI version: unknown")


if __name__ == "__main__":
    app()
