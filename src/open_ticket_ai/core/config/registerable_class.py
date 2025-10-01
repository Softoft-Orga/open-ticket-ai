from open_ticket_ai.core.config.registerable_config import RegisterableConfig


class RegisterableClass:
    def __init__(self, config: RegisterableConfig, *args, **kwargs):
        self.config = config
