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
    confirmationPostingInGroup = State()

    statChoose = State()
    statDay = State()
    statWriteDay = State()
    statLastWeek = State()

    chooseRoleChangeTo = State()
    writeID = State()
    confirmationRoleChanging = State()

    GroupStates = {
        'addCloth': [category, subCategory, brand, name, price, size, condition, photo, confirmationPostingInGroup],
        'statisticsShow': [statChoose, statDay, statWriteDay, statLastWeek],
        'userRoleControl': [chooseRoleChangeTo, writeID, confirmationRoleChanging]
    }
