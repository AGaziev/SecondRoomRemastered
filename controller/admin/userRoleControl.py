from aiogram import types
from aiogram.dispatcher import FSMContext

from ._FSMAdmin import FSMAdmin
from .adminPanel import adminPanel

from model.user.adminControl import authorization
from model.user.userControl import getUserById, getUserRole, getUserListExceptRole, changeUserRole
from model.roles.rolesControl import getRoles
from model.keyboards.adminKeyboardCreator import getRoleChangerKeyboard, getConfirmationKeyboard

from view.senders import adminSender as sender


async def chooseRoleChangeTo(callback: types.CallbackQuery, state: FSMContext):
    if authorization(callback.from_user.id):
        await sender.chooseRoleChangeTo(
            id=callback.message.chat.id,
            rolesChangesToKeyboard=getRoleChangerKeyboard(),
            roles=getRoles()
        )
        await FSMAdmin.panel.set()
    else:
        await sender.permDenied(
            callback.message.chat.id
        )
    await callback.answer()
    await FSMAdmin.chooseRoleChangeTo.set()


async def chooseUser(callback: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        data['roleChangeTo'] = callback.data
        await sender.sendUsersListChangeable(id=callback.message.chat.id,
                                             roleNameChangeTo=data['roleChangeTo'],
                                             usersExceptRole=getUserListExceptRole(data['roleChangeTo']))
    await FSMAdmin.writeID.set()


async def confirmationOfChanging(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        userToChange = getUserById(message.text[1:])
        if userToChange:
            data['userToChangeId'] = message.text[1:]
            await sender.confirmationOfChanging(id=message.chat.id, roleNameChangeTo=data['roleChangeTo'],
                                                userToChange=userToChange,
                                                confirmationKeyboard=getConfirmationKeyboard())
            await FSMAdmin.confirmationRoleChanging.set()
        else:
            await sender.noUserFound(message.chat.id)


async def changingRoleAndReturn(callback: types.callback_query, state: FSMContext):
    async with state.proxy() as data:
        changeUserRole(data['userToChangeId'], data['roleChangeTo'])
        await adminPanel(callback, state)
    await FSMAdmin.panel.set()

async def returnToChoosing(callback: types.callback_query, state: FSMContext):
    async with state.proxy() as data:
        await sender.sendUsersListChangeable(id=callback.message.chat.id,
                                             roleNameChangeTo=data['roleChangeTo'],
                                             usersExceptRole=getUserListExceptRole(data['roleChangeTo']))
        await FSMAdmin.writeID.set()