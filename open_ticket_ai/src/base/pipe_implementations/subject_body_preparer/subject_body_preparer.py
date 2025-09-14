from open_ticket_ai.src.core.config.config_models import ProvidableConfig
from open_ticket_ai.src.core.pipeline.context import PipelineContext
from open_ticket_ai.src.core.pipeline.pipe import Pipe


class SubjectBodyPreparer(Pipe):
    def __init__(self, config: ProvidableConfig):
        super().__init__(config)
        self.preparer_config = config

    def process(self, context: PipelineContext) -> PipelineContext:
        subject_field = self.preparer_config.params.get("subject_field", "subject")
        body_field = self.preparer_config.params.get("body_field", "body")
        repeat_subject = int(self.preparer_config.params.get("repeat_subject", 3))
        result_field = self.preparer_config.params.get("result_field", "subject_body_combined")

        subject = context.data.get(subject_field, "")
        body = context.data.get(body_field, "")

        prepared = f"{subject} " * repeat_subject + body
        context.data[result_field] = prepared.strip()
        return context
