import asyncio
import json
from datetime import datetime, timezone, timedelta
from http.client import responses



from t_invest_api.info_queries import get_instruments, get_tech_analysis



async def is_cross(instrument: dict) -> dict | None:
    from bot import sender
    # with open('instrument.txt', 'a') as in_file:
    #     in_file.write(str(instrument))
    now_time = datetime.now(timezone.utc) # current  time
    three_days_ago = now_time - timedelta(3) # time several days ago

    # receive averages
    average_50, average_200 = await asyncio.gather(
        get_tech_analysis(
        instrument_uid=instrument['uid'],
        to_time= now_time.isoformat(timespec='milliseconds').replace('+00.00', 'Z'),
        from_time=three_days_ago.isoformat(timespec='milliseconds').replace('+00.00', 'Z'),
        length=50
    ),
        get_tech_analysis(
            instrument_uid=instrument['uid'],
            to_time=now_time.isoformat(timespec='milliseconds').replace('+00.00', 'Z'),
            from_time=three_days_ago.isoformat(timespec='milliseconds').replace('+00.00', 'Z'),
            length=200
        )
    )
    if not (average_50 and average_200):
        print('*instrument', instrument)
        print('*average_50.text', average_50.text)
        print('*average_200.text', average_200.text)
        print('*******************')
        return
    try:
        avg_50 = json.loads(average_50.text).get('technicalIndicators') # average of 50th  length
        avg_200 = json.loads(average_200.text).get('technicalIndicators')   #  average of 200th length

        if avg_50 and avg_200: # if averages are  exist
            if (int(avg_50[0]['signal']['units']) < int(avg_200[0]['signal']['units']) and
                    int(avg_50[-1]['signal']['units']) > int(avg_200[-1]['signal']['units'])
            ): # if  averages are crossing:
                print(instrument)
                print('*av_50', avg_50)
                print('*av_200', avg_200)
                await sender(instrument['ticker'])
    except json.decoder.JSONDecodeError as err:
        print('*error', err)



async def search_cross():
    instruments: list = await get_instruments()
    for instrument in instruments:
        result = await is_cross(instrument)
        if result:
            # send_message(result)
            pass

async def main():
    my_responses =  await asyncio.gather(search_cross())

    for response  in my_responses:
        # print(response)
        pass


if __name__ == '__main__':
    asyncio.run(main())
