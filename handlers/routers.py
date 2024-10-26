from aiogram import Router
from  aiogram.filters import Command
from aiogram.types import Message

# try:
#     from  logic.strategy import search_cross
# except ImportError:
#     from ..logic.strategy import search_cross
#
router = Router()
#
@router.message(Command('test'))
async def test(message: Message):
    print('Hello')