from aiogram import types
from config.BotConfig import SHOP_CHANNEL_ID
from view.patterns import adminPatterns as pattern
from repositories.bot import bot


async def permDenied(id):
    return await bot.send_message(id, 'Недостаточно прав')


async def enterAdminPanel(id, adminPanelKeyboard):
    return await bot.send_message(id, text='Успешный вход на панель админа', reply_markup=adminPanelKeyboard)


async def chooseCategory(callback: types.CallbackQuery, categoryKeyboard: types.ReplyKeyboardMarkup):
    await callback.message.edit_text('Добавление вещи...')
    await bot.send_message(chat_id=callback.from_user.id,
                           text='Выберите категорию',
                           reply_markup=categoryKeyboard)
    await callback.answer('start adding new cloth', show_alert=False)


async def chooseSubCategory(id, subCategoryKeyboard):
    await bot.send_message(chat_id=id,
                           text='Выберите подкатегорию',
                           reply_markup=subCategoryKeyboard)


async def chooseProperty(id, nameOfProperty, propertyKeyboard=types.ReplyKeyboardRemove(),
                         isOptional=False):
    await bot.send_message(chat_id=id,
                           text=pattern.getTextForPropertyRequest(nameOfProperty, isOptional),
                           reply_markup=propertyKeyboard)


async def waitForPhoto(id, endAddingKeyboard=types.ReplyKeyboardRemove()):
    await bot.send_message(id,
                           'Загрузите фото',
                           reply_markup=endAddingKeyboard)


async def deletePhoto(photoId: [bool, str], chatId):
    if photoId is False:
        await bot.send_message(chatId, 'Еще ни одного фото не было добавлено')
    else:
        await bot.send_photo(chatId,
                             photoId,
                             caption='Было удалено фото:')


async def endAddingPhoto(id, endAddingKeyboard):
    await bot.send_message(id,
                           'Фото добавлено. Ещё фото?',
                           reply_markup=endAddingKeyboard)


async def postNewClothInChannel(clothInfo: dict):
    await bot.send_media_group(SHOP_CHANNEL_ID,
                               media=pattern.createMediaGroupForPost(clothInfo))


async def statChoose(id, statPeriodKeyboard):
    await bot.send_message(id,
                           pattern.chooseStatShowPeriod(),
                           reply_markup=statPeriodKeyboard)
