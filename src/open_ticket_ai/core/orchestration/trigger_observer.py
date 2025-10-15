import abc


class TriggerObserver(abc.ABC):
    @abc.abstractmethod
    async def on_trigger_fired(self) -> None:
        pass
