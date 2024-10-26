import asyncio
from datetime import datetime, UTC

from logic.strategy import is_overbought
import settings


# from bot import sender


async def run_every_hour(hour=7):
    exec_hour = None
    while True:
        print('*exec_hour', exec_hour)
        print('*excluded_days:', settings.excluded_days)
        print('*excluded_instr:', settings.excluded_instruments)
        hour_now = datetime.now(UTC).hour
        if (settings.start_hour <= hour_now < settings.finish_hour and
            str(datetime.now(UTC).isoweekday()) not in settings.excluded_days and
            exec_hour != hour_now):
            exec_hour  =  hour_now
            from bot import search
            await search()
        await asyncio.sleep(60)

#     from bot import search
#     while True:
#         if datetime.now(UTC).hour == hour:
#             await search()
#             await asyncio.sleep(18000)
#         await asyncio.sleep(1740)

