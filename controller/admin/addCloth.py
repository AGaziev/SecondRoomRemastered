import logging
from datetime import date

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup

from model.cloth.clothManager import addClothToDB
from model.keyboards.adminKeyboardCreator import getClothCategoriesKeyboard, getClothSubCategoriesKeyboard, \
    getConditionKeyboard, isLastPhotoKeyboard, getConfirmationKeyboard
from model.user.adminControl import authorization, canPostInGroup

from view.senders import adminSender as sender
from ._FSMAdmin import FSMAdmin
from .adminPanel import adminPanel


# @dp.callback_query_handler(text='addCloth')
async def startAdding(call: types.CallbackQuery):
    logging.info(f'{authorization(call.from_user.id)} started to add new Cloth')
    await call.answer()
    await sender.chooseCategory(call, getClothCategoriesKeyboard())
    await FSMAdmin.category.set()


async def chooseSubCategory(callback: types.CallbackQuery, state: FSMContext):
    await addPropertyToCloth(state, 'category', callback.data)
    await sender.chooseSubCategory(callback.from_user.id, getClothSubCategoriesKeyboard(callback.data))
    await FSMAdmin.subCategory.set()


async def chooseBrand(callback: types.CallbackQuery, state: FSMContext):
    await addPropertyToCloth(state, 'subCategory', callback.data)
    await sender.chooseProperty(callback.from_user.id, 'бренд', isOptional=True)
    await FSMAdmin.brand.set()


async def chooseName(message: types.Message, state: FSMContext):
    await addPropertyToCloth(state, 'brand', message.text, 'NONAME')
    await sender.chooseProperty(message.from_user.id, 'название', isOptional=True)
    await FSMAdmin.name.set()


# @dp.message_handler(state=FSMAdmin.name)
async def choosePrice(message: types.Message, state: FSMContext):
    await addPropertyToCloth(state, 'name', message.text)
    await sender.chooseProperty(message.from_user.id, 'цену', isOptional=True)
    await FSMAdmin.price.set()


# @dp.message_handler(state=FSMAdmin.price)
async def chooseSize(message: types.Message, state: FSMContext):
    await addPropertyToCloth(state, 'price', message.text)
    await sender.chooseProperty(message.from_user.id, 'размер')
    await FSMAdmin.size.set()


# @dp.message_handler(state=FSMAdmin.size)
async def chooseCondition(message: types.Message, state: FSMContext):
    await addPropertyToCloth(state, 'size', message.text)
    await sender.chooseProperty(message.from_user.id, 'состояние', propertyKeyboard=getConditionKeyboard())
    await FSMAdmin.condition.set()


# @dp.message_handler(state=FSMAdmin.condition)
async def choosePhoto(message: types.Message, state: FSMContext):
    await addPropertyToCloth(state, 'condition', message.text)
    await sender.waitForPhoto(message.from_user.id)
    async with state.proxy() as data:
        data['photo'] = []
    await FSMAdmin.next()


# @dp.message_handler(Text(equals='-'), state=FSMAdmin.photo)
async def deletePhoto(message: types.Message, state: FSMContext):
    await deleteLastPhoto(message, state)
    await sender.waitForPhoto(message.from_user.id, isLastPhotoKeyboard())


# @dp.message_handler(content_types = ['photo'], state=FSMAdmin.photo)
async def endAddingCloth(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['photo'].append(message.photo[0].file_id)
        await sender.endAddingPhoto(message.from_user.id, isLastPhotoKeyboard())


# @dp.callback_query_handler(state=FSMAdmin.photo,text='returnToPanel')
async def returnToAdminPanel(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer()
    async with state.proxy() as data:
        addClothToDB(data)
    await state.finish()
    await adminPanel(callback, state)


async def confirmationOfPosting(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer()
    async with state.proxy() as data:
        data['user'] = callback.from_user.mention
        data['userId'] = callback.from_user.id
        data['date'] = str(date.today())
    await sender.confirmationOfPosting(id=callback.message.chat.id,
                                       confirmationKeyboard=getConfirmationKeyboard())
    await FSMAdmin.confirmationPostingInGroup.set()


async def postingInGroup(callback: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        if canPostInGroup(callback.from_user.id):
            # try:
            await sender.postNewClothInChannel(data)
            # except Exception as e:
            #     logging.error(e)
    await returnToAdminPanel(callback, state)


async def addPropertyToCloth(state: FSMContext, nameOfProperty, propertyInfo, alternativePropertyInfo='None'):
    async with state.proxy() as data:
        if propertyInfo != '-':
            data[nameOfProperty] = propertyInfo
        else:
            data[nameOfProperty] = alternativePropertyInfo


async def deleteLastPhoto(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        try:
            lastPhoto = data['photo'][-1]
            del data['photo'][-1]
        except:
            lastPhoto = False
    await sender.deletePhoto(lastPhoto, message.from_user.id)
