import asyncio
import time
from collections.abc import Awaitable, Callable


async def wait_for_condition(
    check: Callable[[], Awaitable[bool]],
    *,
    timeout: float = 10.0,
    interval: float = 0.1,
    message: str | None = None,
) -> None:
    deadline = time.monotonic() + timeout
    await asyncio.sleep(min(interval, 0.1))

    while True:
        if await check():
            return

        if time.monotonic() >= deadline:
            error_msg = message or f"Timed out after {timeout}s waiting for condition"
            raise AssertionError(error_msg)

        await asyncio.sleep(interval)
