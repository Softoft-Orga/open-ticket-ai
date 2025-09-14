from open_ticket_ai.src.core.config.config_models import ProvidableConfig


class TicketQueueUpdaterConfig(ProvidableConfig):
    confidence_threshold: float
    low_confidence_queue: str
    ticket_system_value2model_values: dict[str, str]
