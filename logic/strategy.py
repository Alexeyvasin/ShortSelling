import asyncio
import json
from datetime import datetime, timezone, timedelta
from http.client import responses

import settings
from bot import sender
from t_invest_api.info_queries import get_instruments, get_tech_analysis



async def is_overbought(instrument: dict, semaphore) -> None:
    async with semaphore:
        now_time = datetime.now(timezone.utc) # current  time
        three_hours_ago = now_time - timedelta(1) # time several days ago

        # receive averages
        rsi_indicator = await asyncio.gather(
            get_tech_analysis(
            instrument_uid=instrument['uid'],
            to_time= now_time.isoformat(timespec='milliseconds').replace('+00.00', 'Z'),
            from_time=three_hours_ago.isoformat(timespec='milliseconds').replace('+00.00', 'Z'),
            length=14
        )
        )
        if not rsi_indicator:
            print('*instrument', instrument)
            print('*rsi.text', rsi_indicator[0].text)
            print('*******************')
            return
        # print(instrument)
        # print(json.loads(rsi[0].text)['technicalIndicators'])
        if res := json.loads(rsi_indicator[0].text)['technicalIndicators']:
            if int(res[-1]['signal']['units']) > 70:
                print(instrument)
                await sender(instrument['ticker'])
                # return res


async def rsi():
    instruments: list = await get_instruments()
    semaphore = asyncio.Semaphore(20)
    coro = (is_overbought(instrument, semaphore)
            for instrument in  instruments
            if instrument['ticker'] not in  settings.excluded_instruments)
    await asyncio.gather(*coro)
    # for instrument in instruments:
    #     result = None
    #
    #     if instrument['ticker'] in settings.excluded_instruments:
    #         pass
    #     else:
    #         result = await is_overbought(instrument)
    #
    #
    #     if result:
    #         print(instrument)
    #         print(result)
    #         await sender(instrument['ticker'])


async def main():
    my_responses =  await asyncio.gather(rsi())

    for response  in my_responses:
        # print(response)
        pass


if __name__ == '__main__':
    asyncio.run(main())
