from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup

from model.cloth.categoriesInfo import getInfoAboutSubcategories
from model.user.adminControl import authorization

backBut = [
    ('Назад', 'back')
]

flipperButs = ['<<', 'Назад', '>>']

def getCategoryKeyboard():
    categoryKeyboard = InlineKeyboardMarkup().add(
        *(InlineKeyboardButton(text, callback_data=text) for text in getInfoAboutSubcategories().keys())) \
        .add(*(InlineKeyboardButton(text, callback_data=data) for text, data in backBut))
    return categoryKeyboard


def getSubCategoryKeyboard(categoryForSearch):
    subcategoriesToShow = []
    for sub, count in getInfoAboutSubcategories()[categoryForSearch].items():
        if count > 0:
            subcategoriesToShow.append(sub)
    return InlineKeyboardMarkup().add(
        *(InlineKeyboardButton(subName, callback_data=subName) for subName in
          subcategoriesToShow)).add(
        *(InlineKeyboardButton(text, callback_data=data) for text, data in backBut))


def getFlipperKeyboard(clientId):
    flipperKb = ReplyKeyboardMarkup(resize_keyboard=True, row_width=3).add(
        *(KeyboardButton(text) for text in flipperButs))
    return flipperKb
