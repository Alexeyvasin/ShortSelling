import os
import logging

from aiogram.types import ReplyKeyboardRemove
from dotenv import load_dotenv

import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext

from handlers.routers import router
from logic.strategy import search_cross

from schedule.every_time import run_every_day

load_dotenv()

token = os.getenv('BOT_TOKEN')

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)

bot = Bot(token=token)

dp = Dispatcher()


async def sender(message):
    await bot.send_message('1091717531', message)



@dp.message(Command('search'))
async def search(message: types.Message=None):
    await sender('Searching is in processing...')
    await search_cross()
    await sender('Searching is finished')


@dp.message(Command("start"))
async def cmd_start(message: types.Message, state: FSMContext):
    await message.answer("Hello!", reply_markup=ReplyKeyboardRemove())
    await state.set_state(None)


# dp.include_router(router)


async def main():
    await asyncio.gather(dp.start_polling(bot), run_every_day(7))


if __name__ == "__main__":
    asyncio.run(main())
