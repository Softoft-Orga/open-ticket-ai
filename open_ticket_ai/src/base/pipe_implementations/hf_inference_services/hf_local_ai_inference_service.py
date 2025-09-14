import os

from open_ticket_ai.src.base.pipe_implementations.hf_inference_services.models import HFLocalAIInferenceServiceInput, \
    HFLocalAIInferenceServiceOutput, HFLocalAIInferenceServiceConfig
from open_ticket_ai.src.base.pipe_implementations.subject_body_preparer.models import SubjectBodyPreparerOutput
from open_ticket_ai.src.core.config.config_models import ProvidableConfig
from open_ticket_ai.src.core.pipeline.context import PipelineContext
from open_ticket_ai.src.core.pipeline.pipe import Pipe


class HFLocalAIInferenceService(
    Pipe[HFLocalAIInferenceServiceConfig, SubjectBodyPreparerOutput, HFLocalAIInferenceServiceOutput]):

    def __init__(self, config: HFLocalAIInferenceServiceConfig):
        super().__init__(config)
        self.ai_inference_config = config

        token_env = config.hf_token_env_var
        token = os.getenv(token_env) if token_env else None

        from transformers import (
            AutoModelForSequenceClassification,
            AutoTokenizer,
            pipeline,
        )

        self.tokenizer = AutoTokenizer.from_pretrained(config.hf_model, token=token)
        model = AutoModelForSequenceClassification.from_pretrained(config.hf_model, token=token)
        self._pipeline = pipeline(
            "text-classification",
            model=model,
            tokenizer=self.tokenizer,
        )

    def process(self, context: PipelineContext[SubjectBodyPreparerOutput]) -> PipelineContext[
        HFLocalAIInferenceServiceOutput]:
        result = self._pipeline(context.data.subject_body_combined)
        new_context = PipelineContext(
            meta_info=context.meta_info,
            data=HFLocalAIInferenceServiceOutput(
                prediction=1,
                confidence=1.0,
                ticket=context.data.ticket,
            )
        )
        return new_context
