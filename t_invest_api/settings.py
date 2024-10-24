import os

from dotenv import load_dotenv

load_dotenv()
token_sandbox = os.getenv('TINKOFF_TOKEN_SANDBOX')

ADDRESS_BASE = 'https://sandbox-invest-public-api.tinkoff.ru'

HEAD = {
    'Authorization': f'Bearer {token_sandbox}',
            'accept': 'application/json',
            'Content-Type': 'application/json'
            }