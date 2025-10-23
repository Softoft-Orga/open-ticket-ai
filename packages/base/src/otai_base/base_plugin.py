from open_ticket_ai.core.injectables.injectable import Injectable
from open_ticket_ai.core.plugins.plugin import CreatePluginFn, Plugin
from packages.base import AddNotePipe, CompositePipe, ExpressionPipe, FetchTicketsPipe, UpdateTicketPipe
from packages.base.src.otai_base.pipes.classification_pipe import ClassificationPipe
from packages.base.src.otai_base.pipes.interval_trigger_pipe import IntervalTrigger
from packages.base.src.otai_base.pipes.orchestrators.simple_sequential_orchestrator import SimpleSequentialOrchestrator
from packages.base.src.otai_base.pipes.pipe_runners.simple_sequential_runner import SimpleSequentialRunner
from packages.base.src.otai_base.template_renderers.jinja_renderer import JinjaRenderer


class BasePlugin(Plugin):
    @property
    def _plugin_name(self) -> str:
        return "otai-base"

    def _get_all_injectables(self) -> list[type[Injectable]]:
        return [
            SimpleSequentialOrchestrator,
            SimpleSequentialRunner,
            AddNotePipe,
            FetchTicketsPipe,
            UpdateTicketPipe,
            ClassificationPipe,
            CompositePipe,
            ExpressionPipe,
            IntervalTrigger,
            JinjaRenderer,
        ]


create_base_plugin: CreatePluginFn = BasePlugin
