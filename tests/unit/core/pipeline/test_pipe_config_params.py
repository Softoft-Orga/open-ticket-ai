from open_ticket_ai.core.pipeline.pipe_config import PipeConfig


def test_pipe_config_params() -> None:
    config: PipeConfig = PipeConfig(id="test", params={"key": "value"})
    assert config.params == {"key": "value"}


def test_pipe_config_params_defaults() -> None:
    config: PipeConfig = PipeConfig(id="test")
    assert config.params == {}
