import typer
from open_ticket_ai.open_ticket_ai.core.plugins.manager import PluginManager

cli = typer.Typer()


def register_plugin_commands():
    plugin_manager = PluginManager()
    plugin_manager.discover_and_load()
    
    for plugin_module in plugin_manager.loaded_plugins:
        if hasattr(plugin_module, 'register_cli_commands'):
            commands = plugin_module.register_cli_commands()
            if isinstance(commands, typer.Typer):
                cli.add_typer(commands)
            elif isinstance(commands, list):
                for command in commands:
                    if isinstance(command, typer.Typer):
                        cli.add_typer(command)


def main():
    register_plugin_commands()
    cli()


if __name__ == "__main__":
    main()
