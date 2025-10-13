import asyncio
import os
from pathlib import Path

import typer
import yaml
from pydantic import ValidationError
from rich.console import Console

from open_ticket_ai.core.config.app_config import AppConfig
from open_ticket_ai.core.config.config_models import RawOpenTicketAIConfig
from open_ticket_ai.main import run


class CLI:
    def __init__(self, app_config: AppConfig | None = None):
        self.app_config = app_config or AppConfig()
        self.console = Console()
        self.app = typer.Typer(help="Open Ticket AI CLI - Manage configurations and templates")
        self._register_commands()

    def _register_commands(self) -> None:
        self.app.command()(self.init)
        self.app.command(name="run")(self.run_app)
        self.app.command(name="check-config")(self.check_config)

        plugin_app = typer.Typer(help="Manage OTAI plugins (future feature)")
        self.app.add_typer(plugin_app, name="plugin")
        plugin_app.command("list")(self._plugin_list_stub)
        plugin_app.command("install")(self._plugin_install_stub)
        plugin_app.command("remove")(self._plugin_remove_stub)

        self.app.command(name="upgrade")(self._upgrade_stub)

    def _get_available_templates(self) -> dict[str, Path]:
        templates_dir = self.app_config.get_templates_dir()

        if not templates_dir.exists():
            return {}

        templates = {}
        for yml_file in templates_dir.glob("*.yml"):
            if yml_file.stem not in ["AGENTS", "QUICK_REFERENCE", "README"]:
                templates[yml_file.stem] = yml_file

        return templates

    def _extract_template_description(self, template_path: Path) -> str:
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

    def init(
        self,
        template: str = typer.Argument(..., help="Template name to initialize from"),
        output: Path = typer.Option("config.yml", "--output", "-o", help="Output file path"),
        force: bool = typer.Option(False, "--force", "-f", help="Overwrite existing file"),
    ) -> None:
        templates = self._get_available_templates()

        if template not in templates:
            self.console.print(f"[red]✗ Template '{template}' not found[/red]")
            self.console.print("\n[yellow]Available templates:[/yellow]")
            for tmpl_name in sorted(templates.keys()):
                self.console.print(f"  • {tmpl_name}")
            raise typer.Exit(1)

        if output.exists() and not force:
            self.console.print(f"[red]✗ File '{output}' already exists. Use --force to overwrite.[/red]")
            raise typer.Exit(1)

        template_path = templates[template]

        try:
            with open(template_path) as src:
                content = src.read()

            with open(output, "w") as dst:
                dst.write(content)

            self.console.print(f"[green]✅ Successfully initialized config from template '{template}'[/green]")
            self.console.print(f"   Created: {output}")
            self.console.print("\n[cyan]📝 Next steps:[/cyan]")
            self.console.print("   1. Edit config.yml to customize your configuration")
            self.console.print("   2. Update environment variables (server addresses, credentials)")
            self.console.print("   3. Validate with: otai check-config config.yml")
            self.console.print("   4. Start with: otai run --config config.yml")

        except Exception as e:
            self.console.print(f"[red]✗ Failed to initialize template: {e}[/red]")
            raise typer.Exit(1) from e

    def run_app(
        self,
        config: Path | None = typer.Option(
            None,
            "--config",
            "-c",
            help="Path to config.yml file (uses OPEN_TICKET_AI_CONFIG env var if not provided)",
        ),
    ) -> None:
        config_path = config

        if config_path is None:
            env_config = os.getenv(self.app_config.config_env_var)
            if env_config:
                config_path = Path(env_config)
            else:
                self.console.print(
                    f"[red]❌ Error: {self.app_config.config_env_var} environment variable not set[/red]"
                )
                self.console.print("\nPlease either:")
                self.console.print(
                    f"  1. Set the environment variable: export {self.app_config.config_env_var}=/path/to/config.yml"
                )
                self.console.print("  2. Use the --config option: otai run --config config.yml")
                raise typer.Exit(1)

        if not config_path.exists():
            self.console.print(f"[red]❌ Error: Config file not found: {config_path}[/red]")
            raise typer.Exit(1)

        self.console.print(f"[green]🚀 Starting Open Ticket AI with config: {config_path}[/green]")

        try:
            asyncio.run(run(str(config_path)))
        except KeyboardInterrupt:
            self.console.print("\n[yellow]⚠ Shutting down...[/yellow]")
        except Exception as e:
            self.console.print(f"[red]❌ Error: {e}[/red]")
            raise typer.Exit(1) from e

    def check_config(
        self,
        config_path: Path = typer.Argument("config.yml", help="Path to config.yml file to validate"),
    ) -> None:
        if not config_path.exists():
            self.console.print(f"[red]❌ Error: Config file not found: {config_path}[/red]")
            raise typer.Exit(1)

        self.console.print(f"[cyan]🔍 Validating config file: {config_path}[/cyan]")

        try:
            with open(config_path) as f:
                raw_config = yaml.safe_load(f)

            config = RawOpenTicketAIConfig.model_validate(raw_config.get(self.app_config.config_yaml_root_key, {}))

            num_plugins = len(config.plugins) if config.plugins else 0
            num_services = len(config.services) if config.services else 0
            num_orchestrator = len(config.orchestrator.runners) if config.orchestrator else 0

            self.console.print("[green]✅ Config file is valid![/green]")
            self.console.print(f"   - Plugins: {num_plugins}")
            self.console.print(f"   - Services: {num_services}")
            self.console.print(f"   - Orchestrator steps: {num_orchestrator}")

        except ValidationError as e:
            self.console.print("[red]❌ Config validation failed:[/red]\n")
            for error in e.errors():
                location = " -> ".join(str(loc) for loc in error["loc"])
                self.console.print(f"  [yellow]{location}:[/yellow] {error['msg']}")
            raise typer.Exit(1) from e
        except yaml.YAMLError as e:
            self.console.print(f"[red]❌ YAML parsing error: {e}[/red]")
            raise typer.Exit(1) from e
        except Exception as e:
            self.console.print(f"[red]❌ Error: {e}[/red]")
            raise typer.Exit(1) from e

    def _plugin_list_stub(self) -> None:
        self.console.print("[yellow]⚠️  Plugin management is not yet implemented[/yellow]")
        self.console.print("This feature will be available in a future version.")
        raise NotImplementedError("Plugin list command will be implemented in a future version")

    def _plugin_install_stub(
        self,
        package_name: str = typer.Argument(..., help="Plugin package name to install"),
        upgrade: bool = typer.Option(False, "--upgrade", "-U", help="Upgrade if already installed"),
    ) -> None:
        self.console.print("[yellow]⚠️  Plugin management is not yet implemented[/yellow]")
        self.console.print("This feature will be available in a future version.")
        raise NotImplementedError("Plugin install command will be implemented in a future version")

    def _plugin_remove_stub(
        self,
        package_name: str = typer.Argument(..., help="Plugin package name to remove"),
        yes: bool = typer.Option(False, "--yes", "-y", help="Skip confirmation prompt"),
    ) -> None:
        self.console.print("[yellow]⚠️  Plugin management is not yet implemented[/yellow]")
        self.console.print("This feature will be available in a future version.")
        raise NotImplementedError("Plugin remove command will be implemented in a future version")

    def _upgrade_stub(
        self,
        check_only: bool = typer.Option(False, "--check-only", help="Only check for updates, don't install"),
    ) -> None:
        self.console.print("[yellow]⚠️  Upgrade command is not yet implemented[/yellow]")
        self.console.print("This feature will be available in a future version.")
        raise NotImplementedError("Upgrade command will be implemented in a future version")


app = CLI().app


def main() -> None:
    app()


if __name__ == "__main__":
    main()
