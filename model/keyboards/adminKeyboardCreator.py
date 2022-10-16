from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, KeyboardButton, InlineKeyboardButton
from model.cloth.categoriesInfo import getInfoAboutCategories, getInfoAboutSubcategories
from model.roles.rolesControl import getRoleNames

adminPanelCheck = {
    'access_statistics': InlineKeyboardButton(text='Статистика', callback_data='statistics'),
    'can_add_clothes': InlineKeyboardButton(text='Добавить вещь', callback_data='addCloth'),
    'can_edit_roles': InlineKeyboardButton(text='Изменить роли', callback_data='editRoles')
}

adminPanelButts = [
    ('Назад', 'back')
]


def getAdminPanelKeyboard(role: dict):
    adminPanelKeyboard = InlineKeyboardMarkup(row_width=3)
    for perm, but in adminPanelCheck.items():
        if role[perm] == True:
            adminPanelKeyboard.add(but)
    adminPanelKeyboard.add(*[InlineKeyboardButton(text=text, callback_data=data) for text, data in adminPanelButts])
    return adminPanelKeyboard


def getClothCategoriesKeyboard():
    categoriesKeyboard = InlineKeyboardMarkup(row_width=3)
    buts = []
    for cat in getInfoAboutCategories().keys():
        buts.append(InlineKeyboardButton(text=cat, callback_data=cat))
    categoriesKeyboard.add(*buts)
    return categoriesKeyboard


def getClothSubCategoriesKeyboard(category):
    subcatKeyboard = InlineKeyboardMarkup(row_width=3)
    buts = []
    for subcat in getInfoAboutSubcategories()[category].keys():
        buts.append(InlineKeyboardButton(text=subcat, callback_data=subcat))
    subcatKeyboard.add(*buts)
    return subcatKeyboard


conditions = [
    'Отличное',
    'Хорошее'
]


def getConditionKeyboard():
    conditionKeyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    for name in conditions:
        conditionKeyboard.add(KeyboardButton(text=name))
    return conditionKeyboard


endAddingPhotoButs = [
    ('Нет', 'endAddingCloth')
]


def isLastPhotoKeyboard():
    return InlineKeyboardMarkup().add(
        *(InlineKeyboardButton(text, callback_data=data) for text, data in endAddingPhotoButs))


statPeriodButs = [
    ('День', 'day'),
    ('За последнюю неделю', 'lastWeek')
]


def getStatPeriodKeyboard():
    return InlineKeyboardMarkup().add(
        *(InlineKeyboardButton(text, callback_data=data) for text, data in statPeriodButs))


def getRoleChangerKeyboard():
    return InlineKeyboardMarkup().add(
        *(InlineKeyboardButton(text, callback_data=text) for text in getRoleNames()))

confirmationButs = [
    ('Да', 'yes'),
    ('Нет', 'no')
]

def getConfirmationKeyboard():
    return InlineKeyboardMarkup().add(
        *(InlineKeyboardButton(text, callback_data=data) for text, data in confirmationButs))