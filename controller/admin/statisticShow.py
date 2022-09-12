from aiogram import types
from aiogram.dispatcher import FSMContext

from ._FSMAdmin import FSMAdmin
from controller.other._FSMOther import FSMOther

from model.user.adminControl import authorization
from model.user.userControl import getUserById, getUserRole
from model.keyboards.otherKeyboardCreator import getMainMenuKeyboard
from model.keyboards.adminKeyboardCreator import getAdminPanelKeyboard

from view.senders import adminSender as sender
from view.senders import otherSender


async def statisticChoose(callback: types.CallbackQuery, state: FSMContext):
    if authorization(callback.from_user.id):
        await sender.enterAdminPanel(
            id=callback.message.chat.id,
            adminPanelKeyboard=getAdminPanelKeyboard(getUserRole(getUserById(callback.from_user.id)))
        )
        await FSMAdmin.panel.set()
    else:
        await sender.permDenied(
            callback.message.chat.id
        )
    await callback.answer()
    await FSMAdmin.panel.set()


async def backToLogin(callback: types.CallbackQuery, state: FSMContext):
    await FSMOther.mainMenu.set()
    user = getUserById(callback.from_user.id)
    await otherSender.login(chatId=callback.from_user.id,
                            mention=user.mention,
                            role=user.role_id,
                            dateOfRegistration=user.date_of_registration,
                            keyboard=getMainMenuKeyboard(getUserRole(user)))
