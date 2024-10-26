import os
import logging

from aiogram.types import ReplyKeyboardRemove
from dotenv import load_dotenv

import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext

# from handlers.routers import router
import settings
from states.states import BotStates

# from logic.strategy import rsi



load_dotenv()

token = os.getenv('BOT_TOKEN')

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)

bot = Bot(token=token)

dp = Dispatcher()

# dp.include_router(router)

async def sender(message, chat_id='1091717531'):
    await bot.send_message(chat_id, message)



@dp.message(Command('search'))
async def search(message: types.Message=None):
    from logic.strategy import rsi
    await sender('The search is in progress...')
    await rsi()
    await sender('The search is finished')


@dp.message(Command("start"))
async def cmd_start(message: types.Message, state: FSMContext):
    await message.answer("Hello!", reply_markup=ReplyKeyboardRemove())
    await state.set_state(None)

@dp.message(Command("test"))
async def test(message: types.Message):
    await message.reply('I am working!')

@dp.message(Command("exclude_days"))
async def exclude_days(message: types.Message, state:FSMContext):
    await bot.send_message(
        message.chat.id,
        f'На данный момент из автопоиска исключены дни:  {''.join(settings.excluded_days)}')
    await message.reply(f'Укажите дни недели (цифрами) которые нужно исключить')
    await state.set_state(BotStates.choosing_days)

@dp.message(StateFilter(BotStates.choosing_days))
async def set_exclude_days(message: types.Message, state: FSMContext):
    if message.text == '0':
        settings.excluded_days = list()

    else:
        settings.excluded_days = list(message.text)
    await bot.send_message(
        message.chat.id,
        f'Исключены следующие дни недели: {settings.excluded_days}')
    await state.set_state(None)

@dp.message(Command('excluded_instrument'))
async def excluded_instruments(message: types.Message, state: FSMContext):
    await bot.send_message(
        message.chat.id,
        f'На данный момент из выдачи исключены следующие инструменты:  {', '.join(settings.excluded_instruments)}')
    await message.reply(
        f'Укажите тикер инструмента для исключения из поиска '
        f'\n(если указать "-" в начале - инструмент удалиться из списка исключений)'
        f'(если указать "0" - список исключений очистится')
    await state.set_state(BotStates.choosing_instruments)

@dp.message(StateFilter(BotStates.choosing_instruments))
async def set_exclude_instruments(message: types.Message, state: FSMContext):
    if message.text == '0':
        settings.excluded_instruments = list()
    elif message.text.startswith('-'):
        settings.excluded_instruments.pop(
            settings.excluded_instruments.index(message.text[1:]))

    else:
        settings.excluded_instruments.append(message.text.strip())
    await bot.send_message(
        message.chat.id,
        f'Исключены следующие инструменты: \n{settings.excluded_instruments}')
    await state.set_state(None)







async def main():
    from schedule.every_time import run_every_hour
    await asyncio.gather(dp.start_polling(bot), run_every_hour(7))


if __name__ == "__main__":
    asyncio.run(main())
