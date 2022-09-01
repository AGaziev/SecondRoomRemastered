from aiogram import types
from aiogram.dispatcher import FSMContext
from model.user.userControl import getUserById, isUserRegistered, registerUser, getUserRole
from model.keyboards.otherKeyboardCreator import getMainMenuKeyboard
from ._FSMOther import FSMOther
from view.senders import otherSender as sender


async def start(message: types.Message, state: FSMContext):
    await state.finish()
    await sender.start(chatId=message.chat.id)
    await login(message, state)


async def login(message: types.Message, state: FSMContext):
    await FSMOther.mainMenu.set()
    user = getUserById(message.from_user.id)
    if not isUserRegistered(message.from_user.id):
        user = registerUser(message.from_user.values)

    await sender.login(chatId=message.chat.id,
                       mention=user.mention,
                       role=user.role_id,
                       dateOfRegistration=user.date_of_registration,
                       keyboard=getMainMenuKeyboard(getUserRole(user)))


async def cancel(message: types.Message, state: FSMContext):
    await state.finish()
    await start(message, state)


