from open_ticket_ai.core.pipeline.configurable_pipe_config import RawPipeConfig, RenderedPipeConfig


class RawHFLocalTextClassificationPipeConfig(RawPipeConfig):
    model: str
    token: str
    prompt: str

class RenderedHFLocalTextClassificationPipeConfig(RenderedPipeConfig):
    model: str
    token: str
    prompt: str