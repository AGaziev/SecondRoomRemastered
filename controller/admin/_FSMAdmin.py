from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup


class FSMAdmin(StatesGroup):
    panel = State()

    category = State()
    subCategory = State()
    brand = State()
    name = State()
    price = State()
    size = State()
    condition = State()
    photo = State()
    GroupStates = {
        'addCloth': [category, subCategory, brand, name, price, size, condition, photo]
    }