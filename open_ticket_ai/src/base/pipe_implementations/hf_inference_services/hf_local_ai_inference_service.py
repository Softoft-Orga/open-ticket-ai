import logging
import os
from functools import lru_cache
from typing import Optional

from injector import inject

from open_ticket_ai.src.base.pipe_implementations.hf_inference_services.models import (
    HFLocalAIInferenceServiceOutput,
)
from open_ticket_ai.src.base.pipe_implementations.subject_body_preparer.models import (
    SubjectBodyPreparerOutput,
)
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

        self.logger = logging.getLogger(self.__class__.__name__)
        self._pipeline = None

    def _get_token(self) -> Optional[str]:
        token_env = self.ai_inference_config.hf_token_env_var
        if not token_env:
            self.logger.warning(
                "No hf_token_env_var configured; proceeding without auth token"
            )
            return None

        token = os.getenv(token_env)
        if not token:
            self.logger.warning(
                f"Environment variable '{token_env}' is not set or empty; proceeding without auth token"
            )
            return None
        if not token.startswith("hf_"):
            self.logger.warning(
                f"Token from '{token_env}' does not appear to be a valid HuggingFace token"
            )
        return token

    @staticmethod
    @lru_cache(maxsize=None)
    def _load_pipeline(model_name: str, token: Optional[str]):
        from transformers import (
            AutoModelForSequenceClassification,
            AutoTokenizer,
            pipeline,
        )

        tokenizer = AutoTokenizer.from_pretrained(model_name, token=token)
        model = AutoModelForSequenceClassification.from_pretrained(
            model_name, token=token
        )
        return pipeline("text-classification", model=model, tokenizer=tokenizer)

    async def process(
        self, context: PipelineContext[SubjectBodyPreparerOutput]
    ) -> PipelineContext[HFLocalAIInferenceServiceOutput]:
        if self._pipeline is None:
            token = self._get_token()
            self._pipeline = self._load_pipeline(
                self.ai_inference_config.hf_model, token
            )

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
