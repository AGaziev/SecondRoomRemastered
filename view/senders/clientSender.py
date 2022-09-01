from aiogram import types

from view.patterns import clientPatterns as pattern
from repositories.bot import bot


async def catalogOpen(userId, categoryInfo, categoryKeyboard, noveltyInfo):
    await bot.send_message(userId,
                           pattern.getCategoryMenu(categoryInfo, noveltyInfo),
                           reply_markup=categoryKeyboard)


async def subcategoryChoose(message: types.Message, subcategoryInfo, subcategoryKeyboard, noveltyInfo, backed=False):
    if not backed:
        await message.edit_text(
            text=pattern.getSubcategoryMenu(subcategoryInfo, noveltyInfo),
            reply_markup=subcategoryKeyboard)
    else:
        await bot.send_message(message.chat.id,
                               text=pattern.getSubcategoryMenu(subcategoryInfo, noveltyInfo),
                               reply_markup=subcategoryKeyboard)


async def startClothShow(userId, flipperKeyboard):
    await bot.send_message(userId, 'Вывод вещей по выбранной категории',
                           reply_markup=flipperKeyboard)


async def showClothAndReturnMessages(userId, cloth, currentClothCount, totalAmountOfClothes):
    return await bot.send_media_group(chat_id=userId,
                                      media=pattern.createMediaGroup(cloth, currentClothCount, totalAmountOfClothes))


async def toStart(userId):
    await bot.send_message(userId, pattern.toStart)

async def backing(userId):
    await bot.send_message(userId, 'Возвращаюсь...', reply_markup=types.ReplyKeyboardRemove())