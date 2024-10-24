import asyncio
from datetime import datetime, UTC

from logic.strategy import search_cross


async def run_every_day(hour=7):
    from bot import search
    while True:
        if datetime.now(UTC).hour == hour:
            await search()
            await asyncio.sleep(18000)
        await asyncio.sleep(1740)

