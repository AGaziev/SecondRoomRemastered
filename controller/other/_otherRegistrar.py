from .mainMenu import *
from config import USED_COMMANDS

def registerHandlers(dp):
    dp.register_message_handler(login, commands=['login'])
    dp.register_message_handler(start, lambda message: message not in USED_COMMANDS)
    dp.register_message_handler(start, state='*', commands=['start', 'help'])
    dp.register_message_handler(cancel, state='*', commands=['cancel'])
