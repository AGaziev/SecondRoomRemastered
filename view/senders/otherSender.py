from repositories.bot import bot
from view.patterns import otherPatterns as pattern
from aiogram.types import ReplyKeyboardRemove

async def start(chatId):
    await bot.send_message(chat_id=chatId,
                           text=pattern.start(),
                           reply_markup=ReplyKeyboardRemove())

async def login(chatId, mention, role, dateOfRegistration, keyboard):
    await bot.send_message(chat_id=chatId,
                           text=pattern.mainMenu(mention, role, dateOfRegistration),
                           reply_markup=keyboard)

