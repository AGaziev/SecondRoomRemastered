from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup


class FSMOther(StatesGroup):
    default = State()
    mainMenu = State()
