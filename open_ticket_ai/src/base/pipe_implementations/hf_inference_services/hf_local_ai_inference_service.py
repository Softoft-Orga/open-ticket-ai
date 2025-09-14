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

        id2label = getattr(self.model.config, "id2label", None) or {}
        self._label2id = {v: int(k) for k, v in id2label.items()} if id2label else {}

    async def process(
        self, context: PipelineContext[SubjectBodyPreparerOutput]
    ) -> PipelineContext[HFLocalAIInferenceServiceOutput]:
        text = context.data.subject_body_combined or ""
        result = self._pipeline(text, truncation=True)
        top = result[0] if isinstance(result, list) else result

        label = top["label"]
        score = float(top["score"])

        pred_id = self._label2id.get(label)
        if pred_id is None and isinstance(label, str) and label.startswith("LABEL_"):
            try:
                pred_id = int(label.split("_", 1)[1])
            except Exception:
                pred_id = None

        prediction_value = pred_id if pred_id is not None else label

        new_context = PipelineContext(
            meta_info=context.meta_info,
            data=HFLocalAIInferenceServiceOutput(
                prediction=prediction_value,
                confidence=score,
                ticket=context.data.ticket,
            ),
        )
        return new_context
