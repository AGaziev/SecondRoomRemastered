from aiogram import Bot
from aiogram.utils.exceptions import ValidationError
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import logging
from config import BOT_TOKEN

fsm = MemoryStorage()
try:
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher(bot, storage=fsm)
except ValidationError:
    logging.fatal('Произошла ошибка при авторизации токена')
    exit()
