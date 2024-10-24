import os

import asyncio
import logging
import json
from datetime import datetime, timezone
from shutil import which

import requests_async
from dotenv import load_dotenv

try:
    from .settings import ADDRESS_BASE, HEAD
except ImportError:
    from settings import ADDRESS_BASE, HEAD

load_dotenv()

async def get_tech_analysis(
        indicator_type='INDICATOR_TYPE_SMA',
        instrument_uid=None,
        ticker='IMOEXF',
        from_time=None,
        to_time=None,
        interval='INDICATOR_INTERVAL_ONE_DAY',
        type_of_price='TYPE_OF_PRICE_CLOSE',
        length=50,
        nano=6,
        units=6,
        fast_length=0,
        slow_length=0,
        signal_smoothing=0

):
    if instrument_uid is  None:
        instrument_uid = (await get_instruments(ticker))[0]['uid']
        print('*uid', instrument_uid)
    if from_time is None:
        from_time = datetime.now(timezone.utc).isoformat(
            timespec='milliseconds'
        ).replace('+00.00', 'Z')
        if to_time is None:
            to_time = datetime.now(timezone.utc).isoformat(
                timespec='milliseconds'
            ).replace('+00.00', 'Z')


    data = {
        'indicatorType': indicator_type,
        'instrumentUid': instrument_uid,
        'from': from_time,
        'to':  to_time,
        'interval': interval,
        'typeOfPrice':  type_of_price,
        'length': length,
        'deviation': {
            'deviationMultiplier': {
                'nano': nano,
                'units': units
            }
        },
        'smoothing': {
            'fastLength': fast_length,
            'slowLength': slow_length,
            'signalSmoothing': signal_smoothing
        }

    }

    address = f'{ADDRESS_BASE}/rest/tinkoff.public.invest.api.contract.v1.MarketDataService/GetTechAnalysis'
    async with requests_async.Session() as session:
        response = await session.post(address, json=data,  headers=HEAD, verify=False)
        return response

async def get_instruments(ticker: str = None) -> list:
    responses = await asyncio.gather(
        get_shares(ticker=ticker),
        get_etfs(ticker=ticker)
    )
    instruments = []
    for response in responses:
        instruments.extend(json.loads(response.text)['instruments'])
    if ticker:
        for instrument in instruments:
            if instrument['ticker'] == ticker.upper():
                return [instrument]
        else:
            return ['Did not find']
    return instruments

async def get_shares(ticker=None) -> dict:
    address = f'{ADDRESS_BASE}/rest/tinkoff.public.invest.api.contract.v1.InstrumentsService/Shares'
    data = {
        "instrumentStatus": "INSTRUMENT_STATUS_UNSPECIFIED",
        "instrumentExchange": "INSTRUMENT_EXCHANGE_UNSPECIFIED"
    }

    answer = await requests_async.post(address, json=data, headers=HEAD, verify=False)

    return answer

async def get_etfs(ticker=None) -> dict:
    address = f'{ADDRESS_BASE}/rest/tinkoff.public.invest.api.contract.v1.InstrumentsService/Etfs'
    data = {
        "instrumentStatus": "INSTRUMENT_STATUS_UNSPECIFIED",
        "instrumentExchange": "INSTRUMENT_EXCHANGE_UNSPECIFIED"
    }

    answer = await requests_async.post(address, json=data, headers=HEAD, verify=False)

    return answer

async def main():
    responses = await asyncio.gather(get_tech_analysis(ticker='MOEX'))


if __name__ == "__main__":
    asyncio.run(main())