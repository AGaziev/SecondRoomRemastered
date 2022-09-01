from .catalog import *
from controller.other._FSMOther import FSMOther
from ._FSMClient import FSMClient
from aiogram.dispatcher.filters import Text


def registerHandlers(dp):
    dp.register_message_handler(catalogEvent, commands=['catalog'], state='*')
    dp.register_callback_query_handler(catalogEvent, state=FSMOther.mainMenu, text='catalog')
    dp.register_callback_query_handler(subcategorySelect, state=FSMClient.categorySelect, text=['Обувь', 'Верх', 'Низ'])
    dp.register_callback_query_handler(backCallback, state=FSMClient.states, text='back')
    dp.register_callback_query_handler(showClothes, state=FSMClient.subCategorySelect)
    dp.register_message_handler(getAnother, text=['<<', '>>'], state=FSMClient.showClothes)
    dp.register_message_handler(deleteCloth, Text(equals=['удалить', 'delete', 'udalit'], ignore_case=True))
    dp.register_message_handler(back, Text(equals='Назад', ignore_case=True), state=FSMClient.showClothes)