import logging
import os

from injector import inject

from open_ticket_ai.src.base.pipe_implementations.hf_inference_services.models import HFLocalAIInferenceServiceOutput
from open_ticket_ai.src.base.pipe_implementations.subject_body_preparer.models import SubjectBodyPreparerOutput
from open_ticket_ai.src.core.config.config_models import OpenTicketAIConfig
from open_ticket_ai.src.core.pipeline.context import PipelineContext
from open_ticket_ai.src.core.pipeline.pipe import Pipe


class HFLocalAIInferenceService(
    Pipe[SubjectBodyPreparerOutput, HFLocalAIInferenceServiceOutput]
):
    InputModel = SubjectBodyPreparerOutput
    OutputModel = HFLocalAIInferenceServiceOutput

    @inject
    def __init__(self, config: OpenTicketAIConfig):
        super().__init__(config)
        self.ai_inference_config = config

        token_env = config.hf_token_env_var
        token = os.getenv(token_env) if token_env else None

        from transformers import AutoModelForSequenceClassification, AutoTokenizer, pipeline

        self.tokenizer = AutoTokenizer.from_pretrained(config.hf_model, token=token)
        self.model = AutoModelForSequenceClassification.from_pretrained(config.hf_model, token=token)
        self._pipeline = pipeline("text-classification", model=self.model, tokenizer=self.tokenizer)
        self.logger = logging.getLogger(self.__class__.__name__)

    async def process(
        self, context: PipelineContext[SubjectBodyPreparerOutput]
    ) -> PipelineContext[HFLocalAIInferenceServiceOutput]:
        text = context.data.subject_body_combined or ""
        result = self._pipeline(text, truncation=True)
        top = result[0] if isinstance(result, list) else result

        label = top["label"]
        score = float(top["score"])

        self.logger.info(f"Prediction: label {label} with score {score}")
        new_context = PipelineContext(
            meta_info=context.meta_info,
            data=HFLocalAIInferenceServiceOutput(
                prediction=label,
                confidence=score,
                ticket=context.data.ticket,
            ),
        )
        return new_context
