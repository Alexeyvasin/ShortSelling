from aiogram.fsm.state import State, StatesGroup

class BotStates(StatesGroup):
    choosing_days = State()
    choosing_instruments = State()