from aiogram import Router, F
from  aiogram.filters import Command
from aiogram.types import Message

# try:
#     from  logic.strategy import search_cross
# except ImportError:
#     from ..logic.strategy import search_cross
#
router = Router()
#
# @router.message(Command('search'))
# async def search(message: Message):
#     await search_cross()