from injector import inject

from open_ticket_ai.src.base.pipe_implementations.subject_body_preparer.models import SubjectBodyPreparerOutput
from open_ticket_ai.src.base.pipe_implementations.ticket_fetcher.models import QueueTicketFetcherOutput
from open_ticket_ai.src.core.config.config_models import OpenTicketAIConfig
from open_ticket_ai.src.core.pipeline.context import PipelineContext
from open_ticket_ai.src.core.pipeline.pipe import Pipe


class SubjectBodyPreparer(Pipe[QueueTicketFetcherOutput, SubjectBodyPreparerOutput]):
    InputModel = QueueTicketFetcherOutput
    OutputModel = SubjectBodyPreparerOutput
    @inject
    def __init__(self, config: OpenTicketAIConfig):
        super().__init__(config)

    async def process(self, context: PipelineContext[QueueTicketFetcherOutput]) -> PipelineContext[
        SubjectBodyPreparerOutput]:
        subject = context.data.ticket.subject
        body = context.data.ticket.body

        prepared = subject + body
        new_context = PipelineContext(
            meta_info=context.meta_info,
            data=SubjectBodyPreparerOutput(
                subject_body_combined=prepared,
                ticket=context.data.ticket,
            )
        )
        return new_context
