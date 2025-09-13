from pydantic import BaseModel


class TextAIModelInput(BaseModel):
    """
    Context for the input to the Hugging Face inference service.

    This class is used to encapsulate the input data and any additional parameters
    required for the inference request.

    Attributes:
        ai_model_input (str): The input text provided to the AI model for processing.
            Represents the primary data payload for the inference request.
    """
    ai_model_input: str