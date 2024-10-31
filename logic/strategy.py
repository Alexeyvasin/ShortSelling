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
        res = rsi_indicator[0]
        print('*res', res)
        if not res:
            print('*instrument', instrument)
            print('*res', res)
            print('*******************')
            return
        # print(instrument)
        # print(json.loads(rsi[0].text)['technicalIndicators'])
        else:
            try:
                if res := json.loads(res)['technicalIndicators']:
                    if int(res[-1]['signal']['units']) > 70:
                        print(instrument)
                        await sender(instrument['ticker'])
                        # return res
            except:
                pass

async def rsi():
    instruments: list = await get_instruments()
    semaphore = asyncio.Semaphore(15)
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
