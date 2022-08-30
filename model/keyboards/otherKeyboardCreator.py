from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup

mainMenuCheck = {
    'access_catalog': InlineKeyboardButton(text='Каталог', callback_data='catalog'),
    'access_admin_panel': InlineKeyboardButton(text='Админка', callback_data='adminPanel')
}

mainMenuButts = [
    ('Инфо', 'info')
]


def getMainMenuKeyboard(role: dict):
    mainMenuKeyboard = InlineKeyboardMarkup(row_width=3)
    for perm, but in mainMenuCheck.items():
        if role[perm] is True:
            mainMenuKeyboard.add(but)
    mainMenuKeyboard.add(*[InlineKeyboardButton(text=text, callback_data=data) for text, data in mainMenuButts])
    return mainMenuKeyboard
