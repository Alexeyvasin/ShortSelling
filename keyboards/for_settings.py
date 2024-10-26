from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder

def get_inst_kb() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text='1')
    kb.button(text='2')
    kb.adjust(1)
    return kb.as_markup(resize_keyboard=True)