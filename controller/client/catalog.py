from aiogram import types
from aiogram.dispatcher import FSMContext
from ._FSMClient import FSMClient
from controller.other._FSMOther import FSMOther

from view.senders import clientSender as sender
from view.senders import otherSender

from model.cloth.categoriesInfo import categoriesWithNew, subcatWithNew, \
    getInfoAboutCategories, getInfoAboutSubcategories
from model.keyboards.clientKeyboardCreator import getCategoryKeyboard, getSubCategoryKeyboard, getFlipperKeyboard
from model.keyboards.otherKeyboardCreator import getMainMenuKeyboard
from model.novelty import noveltyControl
from model.cloth.clothManager import getClothesList, deleteClothFromDB
from model.user.userControl import getUserById, getUserRole


async def backCallback(callback: types.CallbackQuery, state: FSMContext):
    await back(callback.message, state)
    await callback.answer()


async def back(message: types.Message, state: FSMContext):
    await sender.backing(message.chat.id)
    stateInfo = await state.get_state()
    if stateInfo == "FSMClient:showClothes":
        async with state.proxy() as show:
            await sender.subcategoryChoose(message,
                                           subcategoryInfo=getInfoAboutSubcategories()[show['category']],
                                           subcategoryKeyboard=getSubCategoryKeyboard(
                                               show['category']),
                                           noveltyInfo=subcatWithNew(message.chat.id),
                                           backed=True)
            await FSMClient.previous()
    elif stateInfo == "FSMClient:subCategorySelect":
        await message.delete()
        await sender.catalogOpen(message.chat.id,
                                 noveltyInfo=categoriesWithNew(message.chat.id),
                                 categoryInfo=getInfoAboutCategories(),
                                 categoryKeyboard=getCategoryKeyboard())
        await FSMClient.previous()
    else:
        await FSMOther.mainMenu.set()
        user = getUserById(message.chat.id)
        await otherSender.login(chatId=message.chat.id,
                           mention=user.mention,
                           role=user.role_id,
                           dateOfRegistration=user.date_of_registration,
                           keyboard=getMainMenuKeyboard(getUserRole(user)))



async def catalogEvent(callback: [types.CallbackQuery, types.Message], state: FSMContext):
    if type(callback) == types.CallbackQuery:
        await callback.answer()
    if not getUserById(callback.from_user.id).role_id.access_catalog:
        return
    await FSMClient.categorySelect.set()
    await sender.catalogOpen(callback.from_user.id,
                             noveltyInfo=categoriesWithNew(callback.from_user.id),
                             categoryInfo=getInfoAboutCategories(),
                             categoryKeyboard=getCategoryKeyboard())


async def subcategorySelect(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer()
    async with state.proxy() as show:
        show['category'] = callback.data
    await FSMClient.subCategorySelect.set()
    await sender.subcategoryChoose(callback.message,
                                   subcategoryInfo=getInfoAboutSubcategories()[show['category']],
                                   subcategoryKeyboard=getSubCategoryKeyboard(show['category']),
                                   noveltyInfo=subcatWithNew(callback.from_user.id))


async def showClothes(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer()
    async with state.proxy() as show:
        # TODO SUBCATEGORIES STATISTICS INCR
        show['subCategory'] = callback.data
        noveltyControl.notNewAnymore(callback.from_user.id, show['category'], show['subCategory'])
        show['clothes'] = getClothesList(show['category'], show['subCategory'])
        show['currentCloth'] = 0
        show['currentClothId'] = show['clothes'][show['currentCloth']]['id']
        show['countOfCloths'] = len(show['clothes'])
        await sender.startClothShow(userId=callback.from_user.id,
                                    flipperKeyboard=getFlipperKeyboard(callback.from_user.id))
        await sendCurrentCloth(callback.from_user.id, show)
        await FSMClient.showClothes.set()


async def getAnother(message: types.Message, state: FSMContext):
    async with state.proxy() as show:
        current = show['currentCloth']
        for msg in show['currentClothMessages']:
            await msg.delete()
        if message.text == '<<':
            show['currentCloth'] = await checkIter(current - 1, show['countOfCloths'])
        elif message.text == '>>':
            show['currentCloth'] = await checkIter(current + 1, show['countOfCloths'])
        await sendCurrentCloth(message.from_user.id, show)


async def deleteCloth(message: types.Message, state: FSMContext):
    async with state.proxy() as show:
        if not getUserById(message.from_user.id).role_id.can_delete_all or \
                not show['currentCloth']['userId'] == message.from_user.id:
            return
        deleteClothFromDB(show['category'], show['subCategory'], show['currentClothId'])
        show['clothes'] = getClothesList(show['category'], show['subCategory'])
        for msg in show['currentClothMessages']:
            await msg.delete()
        if show['countOfCloths'] == 1:
            await sender.subcategoryChoose(message,
                                           subcategoryInfo=getInfoAboutSubcategories()[show['category']],
                                           subcategoryKeyboard=getSubCategoryKeyboard(
                                               show['category']),
                                           noveltyInfo=subcatWithNew(message.from_user.id),
                                           backed=True)
            await FSMClient.previous()
            return
        else:
            show['countOfCloths'] -= 1
            show['currentCloth'] = await checkIter(show['currentCloth'] - 1, show['countOfCloths'])
            await sendCurrentCloth(message.from_user.id, show)


async def sendCurrentCloth(userId, show):
    cloth = show['clothes'][show['currentCloth']]
    show['currentClothId'] = show['clothes'][show['currentCloth']]['id']
    show['currentClothMessages'] = \
        list(await sender.showClothAndReturnMessages(userId,
                                                     cloth=cloth,
                                                     currentClothCount=show['currentCloth'] + 1,
                                                     totalAmountOfClothes=show['countOfCloths']))


async def checkIter(current, total):
    if current < 0:
        return total - 1
    elif current == total:
        return 0
    else:
        return current
