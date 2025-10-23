import logging
import os
from collections.abc import Callable
from functools import lru_cache
from typing import Any, ClassVar

import transformers
from huggingface_hub import HfApi, login
from open_ticket_ai.core.base_model import StrictBaseModel
from open_ticket_ai.core.injectables.injectable import Injectable
from open_ticket_ai.core.injectables.injectable_models import InjectableConfig
from open_ticket_ai.core.logging.logging_iface import LoggerFactory
from otai_base.ai_classification_services.classification_models import ClassificationRequest, ClassificationResult
from pydantic import BaseModel, Field
from transformers import (
    AutoModelForSequenceClassification,
    AutoTokenizer,
    Pipeline,
    pipeline,
)

hf_logger = logging.getLogger("hf_local_detailed")
hf_logger.setLevel(logging.DEBUG)

# Optional: log to console too
if not hf_logger.hasHandlers():
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
    hf_logger.addHandler(handler)

TEXT_PREVIEW_LIMIT = 100


@lru_cache(maxsize=16)
def _get_hf_pipeline(model: str, token: str | None):
    hf_logger.info("=== 🧠 HUGGINGFACE PIPELINE LOADING START ===")
    hf_logger.info(f"Model name: {model}")
    hf_logger.info(f"Transformers version: {transformers.__version__}")
    hf_logger.info(f"Env CWD: {os.getcwd()}")
    hf_logger.info("Env variables snapshot:")

    for key in [
        "HF_TOKEN",
        "HUGGING_FACE_HUB_TOKEN",
        "HF_HUB_TOKEN",
        "HUGGING_FACE_TOKEN",
    ]:
        value = os.getenv(key)
        if value:
            hf_logger.info(f"  {key}: {value[:10]}...{value[-5:]}")
        else:
            hf_logger.info(f"  {key}: (not set)")

    if token:
        hf_logger.info(f"Token parameter provided: {token[:10]}...{token[-5:]}")
    else:
        hf_logger.warning("⚠️ No token passed explicitly to _get_hf_pipeline()")

    # Login handling
    active_token = token or os.getenv("HF_TOKEN") or os.getenv("HUGGING_FACE_HUB_TOKEN")

    if active_token:
        try:
            login(token=active_token, add_to_git_credential=False)
            hf_logger.info("✅ Successfully logged into Hugging Face Hub")
        except Exception:
            hf_logger.exception("❌ Hugging Face login failed")
    else:
        hf_logger.warning("⚠️ No active token found at all. Login skipped.")

    # Check current HF user
    try:
        api = HfApi()
        user = api.whoami(token=active_token)
        hf_logger.info(f"👤 Logged in as: {user.get('name')} (id={user.get('id')})")
    except Exception as e:
        hf_logger.warning(f"⚠️ Could not fetch current HF user info: {e}")

    # Pick correct argument name
    param_name = "token" if transformers.__version__ >= "4.44.0" else "use_auth_token"
    hf_logger.info(f"Parameter used for auth: {param_name}")

    try:
        if param_name == "token":
            tokenizer = AutoTokenizer.from_pretrained(model, token=active_token)
            loaded_model = AutoModelForSequenceClassification.from_pretrained(model, token=active_token)
        else:
            tokenizer = AutoTokenizer.from_pretrained(model, use_auth_token=active_token)
            loaded_model = AutoModelForSequenceClassification.from_pretrained(model, use_auth_token=active_token)
        hf_logger.info("✅ Model + tokenizer successfully loaded")
    except Exception as e:
        hf_logger.error(f"❌ Failed to load model: {e}", exc_info=True)
        raise

    pipe = pipeline("text-classification", model=loaded_model, tokenizer=tokenizer)
    hf_logger.info(f"✅ Pipeline created successfully for model: {model}")
    hf_logger.info("=== ✅ HUGGINGFACE PIPELINE READY ===")

    return pipe


type GetPipelineFunc = Callable[[str, str | None], Pipeline]


class HFClassificationServiceParams(StrictBaseModel):
    api_token: str | None = Field(
        default=None,
        description="Optional HuggingFace API token for accessing private models or increased rate limits.",
    )


class HFClassificationService(Injectable[HFClassificationServiceParams]):
    ParamsModel: ClassVar[type[BaseModel]] = HFClassificationServiceParams

    def __init__(
        self,
        config: InjectableConfig,
        logger_factory: LoggerFactory,
        get_pipeline: GetPipelineFunc = _get_hf_pipeline,
        *args: Any,
        **kwargs: Any,
    ):
        super().__init__(config, logger_factory, *args, **kwargs)
        self._get_pipeline = get_pipeline
        self._logger.info("🤗 HFClassificationService initialized")

    def classify(self, classification_request: ClassificationRequest) -> ClassificationResult:
        classification_request = classification_request.model_copy(
            update={"api_token": classification_request.api_token or self._params.api_token}
        )
        self._logger.info(f"🚀 Starting classification request {classification_request.model_dump()}")
        self._logger.info(f"🤖 Running HuggingFace classification with model: {classification_request.model_name}")
        text_preview = (
            classification_request.text[:TEXT_PREVIEW_LIMIT] + "..."
            if len(classification_request.text) > TEXT_PREVIEW_LIMIT
            else classification_request.text
        )
        self._logger.debug(f"Text preview: {text_preview}")

        classify: Pipeline = self._get_pipeline(classification_request.model_name, classification_request.api_token)
        self._logger.debug("Pipeline obtained, running classification...")

        classifications: Any = classify(classification_request.text, truncation=True)

        if not classifications:
            self._logger.error("❌ No classification result returned from HuggingFace pipeline")
            raise ValueError("No classification result returned from HuggingFace pipeline")

        if not isinstance(classifications, list):
            self._logger.error(f"❌ HuggingFace pipeline returned non-list result: {type(classifications)}")
            raise TypeError("HuggingFace pipeline returned a non-list result")

        classification = classifications[0]
        result = ClassificationResult(label=classification["label"], confidence=classification["score"])

        self._logger.info(f"✅ Classification complete: {result.label} (confidence: {result.confidence:.4f})")
        self._logger.debug(f"Full classification result: {classification}")

        return result

    async def aclassify(self, req: ClassificationRequest) -> ClassificationResult:
        self._logger.debug("Async classification requested, delegating to sync classify")
        return self.classify(req)
