import importlib.metadata as md
import logging
import subprocess
import sys

import typer

from open_ticket_ai.open_ticket_ai.core.plugins.manager import PLUGIN_GROUP

cli = typer.Typer()
plugin = typer.Typer()
cli.add_typer(plugin, name="plugin")


@plugin.command("list")
def plugin_list():
    try:
        entry_points = md.entry_points(group=PLUGIN_GROUP)
        
        if not entry_points:
            typer.echo("No plugins installed.")
            return
        
        typer.echo("Installed plugins:")
        for ep in entry_points:
            try:
                plugin_module = ep.load()
                meta = getattr(plugin_module, "get_metadata", lambda: {})()
                
                name = meta.get("name", ep.name)
                version = meta.get("version", "unknown")
                description = meta.get("description", "No description")
                core_api = meta.get("core_api", "unknown")
                
                typer.echo(f"\n  • {name}")
                typer.echo(f"    Version: {version}")
                typer.echo(f"    Core API: {core_api}")
                typer.echo(f"    Description: {description}")
            except Exception as e:
                typer.echo(f"\n  • {ep.name} (Error loading: {e})")
    except Exception as e:
        typer.echo(f"Error listing plugins: {e}", err=True)
        raise typer.Exit(code=1)


@plugin.command("install")
def plugin_install(plugin_name: str):
    try:
        typer.echo(f"Installing plugin: {plugin_name}")
        result = subprocess.run(
            [sys.executable, "-m", "pip", "install", plugin_name],
            capture_output=True,
            text=True,
            check=False
        )
        
        if result.returncode == 0:
            typer.echo(f"✓ Plugin '{plugin_name}' installed successfully.")
        else:
            typer.echo(f"✗ Failed to install plugin '{plugin_name}'.", err=True)
            typer.echo(result.stderr, err=True)
            raise typer.Exit(code=1)
    except typer.Exit:
        raise
    except Exception as e:
        typer.echo(f"Error installing plugin: {e}", err=True)
        raise typer.Exit(code=1)


@plugin.command("remove")
def plugin_remove(plugin_name: str):
    try:
        typer.echo(f"Removing plugin: {plugin_name}")
        result = subprocess.run(
            [sys.executable, "-m", "pip", "uninstall", "-y", plugin_name],
            capture_output=True,
            text=True,
            check=False
        )
        
        if result.returncode == 0:
            typer.echo(f"✓ Plugin '{plugin_name}' removed successfully.")
        else:
            typer.echo(f"✗ Failed to remove plugin '{plugin_name}'.", err=True)
            typer.echo(result.stderr, err=True)
            raise typer.Exit(code=1)
    except typer.Exit:
        raise
    except Exception as e:
        typer.echo(f"Error removing plugin: {e}", err=True)
        raise typer.Exit(code=1)


def discover_and_register_plugin_commands():
    logger = logging.getLogger(__name__)
    
    try:
        for ep in md.entry_points(group=PLUGIN_GROUP):
            try:
                plugin_module = ep.load()
                
                if hasattr(plugin_module, "register_cli_commands"):
                    plugin_commands = plugin_module.register_cli_commands()
                    
                    if isinstance(plugin_commands, typer.Typer):
                        cli.add_typer(plugin_commands)
                    elif isinstance(plugin_commands, dict):
                        for cmd_name, cmd in plugin_commands.items():
                            if isinstance(cmd, typer.Typer):
                                cli.add_typer(cmd, name=cmd_name)
                    elif isinstance(plugin_commands, list):
                        for cmd in plugin_commands:
                            if isinstance(cmd, typer.Typer):
                                cli.add_typer(cmd)
            except Exception:
                logger.debug(f"Plugin '{ep.name}' does not expose CLI commands or failed to load")
    except Exception:
        logger.debug("Error discovering plugin CLI commands")


discover_and_register_plugin_commands()


def main():
    cli()


if __name__ == "__main__":
    main()
