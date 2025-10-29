from open_ticket_ai import Injectable, Plugin

from otai_base.pipes.classification_pipe import ClassificationPipe
from otai_base.pipes.composite_pipe import CompositePipe
from otai_base.pipes.expression_pipe import ExpressionPipe
from otai_base.pipes.interval_trigger_pipe import IntervalTrigger
from otai_base.pipes.orchestrators.simple_sequential_orchestrator import SimpleSequentialOrchestrator
from otai_base.pipes.pipe_runners.simple_sequential_runner import SimpleSequentialRunner
from otai_base.pipes.ticket_system_pipes import AddNotePipe, FetchTicketsPipe, UpdateTicketPipe
from otai_base.template_renderers.jinja_renderer import JinjaRenderer


class BasePlugin(Plugin):
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
