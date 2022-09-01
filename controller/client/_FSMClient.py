from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

class FSMClient(StatesGroup):
    categorySelect = State()
    subCategorySelect = State()
    showClothes = State()