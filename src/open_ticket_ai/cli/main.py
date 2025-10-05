import importlib.metadata as md
import logging
import subprocess
import sys

import click

from open_ticket_ai.core.plugins.manager import PLUGIN_GROUP


@click.group()
@click.version_option()
def cli():
    pass


@cli.group()
def plugin():
    pass


@plugin.command("list")
def plugin_list():
    try:
        entry_points = md.entry_points(group=PLUGIN_GROUP)
        
        if not entry_points:
            click.echo("No plugins installed.")
            return
        
        click.echo("Installed plugins:")
        for ep in entry_points:
            try:
                plugin_module = ep.load()
                meta = getattr(plugin_module, "get_metadata", lambda: {})()
                
                name = meta.get("name", ep.name)
                version = meta.get("version", "unknown")
                description = meta.get("description", "No description")
                core_api = meta.get("core_api", "unknown")
                
                click.echo(f"\n  • {name}")
                click.echo(f"    Version: {version}")
                click.echo(f"    Core API: {core_api}")
                click.echo(f"    Description: {description}")
            except Exception as e:
                click.echo(f"\n  • {ep.name} (Error loading: {e})")
    except Exception as e:
        click.echo(f"Error listing plugins: {e}", err=True)
        sys.exit(1)


@plugin.command("install")
@click.argument("plugin_name")
def plugin_install(plugin_name):
    try:
        click.echo(f"Installing plugin: {plugin_name}")
        result = subprocess.run(
            [sys.executable, "-m", "pip", "install", plugin_name],
            capture_output=True,
            text=True,
            check=False
        )
        
        if result.returncode == 0:
            click.echo(f"✓ Plugin '{plugin_name}' installed successfully.")
        else:
            click.echo(f"✗ Failed to install plugin '{plugin_name}'.", err=True)
            click.echo(result.stderr, err=True)
            sys.exit(1)
    except Exception as e:
        click.echo(f"Error installing plugin: {e}", err=True)
        sys.exit(1)


@plugin.command("remove")
@click.argument("plugin_name")
def plugin_remove(plugin_name):
    try:
        click.echo(f"Removing plugin: {plugin_name}")
        result = subprocess.run(
            [sys.executable, "-m", "pip", "uninstall", "-y", plugin_name],
            capture_output=True,
            text=True,
            check=False
        )
        
        if result.returncode == 0:
            click.echo(f"✓ Plugin '{plugin_name}' removed successfully.")
        else:
            click.echo(f"✗ Failed to remove plugin '{plugin_name}'.", err=True)
            click.echo(result.stderr, err=True)
            sys.exit(1)
    except Exception as e:
        click.echo(f"Error removing plugin: {e}", err=True)
        sys.exit(1)


def discover_and_register_plugin_commands():
    logger = logging.getLogger(__name__)
    
    try:
        for ep in md.entry_points(group=PLUGIN_GROUP):
            try:
                plugin_module = ep.load()
                
                if hasattr(plugin_module, "register_cli_commands"):
                    plugin_commands = plugin_module.register_cli_commands()
                    
                    if isinstance(plugin_commands, click.Command):
                        cli.add_command(plugin_commands)
                    elif isinstance(plugin_commands, dict):
                        for cmd_name, cmd in plugin_commands.items():
                            cli.add_command(cmd, name=cmd_name)
                    elif isinstance(plugin_commands, list):
                        for cmd in plugin_commands:
                            if isinstance(cmd, click.Command):
                                cli.add_command(cmd)
            except Exception:
                logger.debug(f"Plugin '{ep.name}' does not expose CLI commands or failed to load")
    except Exception:
        logger.debug("Error discovering plugin CLI commands")


discover_and_register_plugin_commands()


if __name__ == "__main__":
    cli()
