import click
from open_ticket_ai.core.plugins.manager import PluginManager


@click.group()
@click.version_option()
def cli():
    pass


def register_plugin_commands():
    plugin_manager = PluginManager()
    plugin_manager.discover_and_load()
    
    for plugin_module in plugin_manager.loaded_plugins:
        if hasattr(plugin_module, 'register_cli_commands'):
            commands = plugin_module.register_cli_commands()
            for command in commands:
                cli.add_command(command)


def main():
    register_plugin_commands()
    cli()


if __name__ == "__main__":
    main()
