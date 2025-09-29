from __future__ import annotations

import abc
from abc import abstractmethod
from typing import Any

from ..config.registerable import RegisterableClass, RawRegisterableConfig, RenderedRegistrableConfig


class BasePipe[RawPipeConfigT: RawRegisterableConfig, RenderedPipeConfigT: RenderedRegistrableConfig](
    RegisterableClass[RawPipeConfigT, RenderedPipeConfigT], abc.ABC
):

    @abstractmethod
    async def _process(self) -> dict[str, Any]:
        pass
