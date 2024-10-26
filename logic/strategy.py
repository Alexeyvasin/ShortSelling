import asyncio
import json
from datetime import datetime, timezone, timedelta
from http.client import responses

import settings
from bot import sender
from t_invest_api.info_queries import get_instruments, get_tech_analysis



async def is_overbought(instrument: dict) -> dict | None:
    now_time = datetime.now(timezone.utc) # current  time
    three_hours_ago = now_time - timedelta(1) # time several days ago

    # receive averages
    rsi = await asyncio.gather(
        get_tech_analysis(
        instrument_uid=instrument['uid'],
        to_time= now_time.isoformat(timespec='milliseconds').replace('+00.00', 'Z'),
        from_time=three_hours_ago.isoformat(timespec='milliseconds').replace('+00.00', 'Z'),
        length=14
    )
    )
    if not rsi:
        print('*instrument', instrument)
        print('*rsi.text', rsi[0].text)
        print('*******************')
        return
    # print(instrument)
    # print(json.loads(rsi[0].text)['technicalIndicators'])
    if res := json.loads(rsi[0].text)['technicalIndicators']:
        if int(res[-1]['signal']['units']) > 70:
            return res


async def rsi():
    instruments: list = await get_instruments()
    for instrument in instruments:
        if instrument['ticker'] in settings.excluded_instruments:
            return
        result = await is_overbought(instrument)


        if result:
            print(instrument)
            print(result)
            await sender(instrument['ticker'])


async def main():
    my_responses =  await asyncio.gather(rsi())

    for response  in my_responses:
        # print(response)
        pass


if __name__ == '__main__':
    asyncio.run(main())
