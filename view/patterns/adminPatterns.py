from aiogram import types
from datetime import date

adminGreeting = 'Успешный вход на панель админа'

authorizationRejection = 'Недостаточно прав'


def getTextForPropertyRequest(name, isOptional=False):
    text = f'Напишите {name}'
    if isOptional:
        text += '(\'-\' для пропуска)'
    return text


def getClothInfoForChannel(data: dict):
    try:
        userMention = f"<a href=\"tg://user?id={data['userId']}\">{data['user']}</a>"
    except:
        userMention = data['user']
    name = (f'\"{data["name"]}\"' if data["name"] != 'None' else '')
    return f'{data["brand"]}\n\n' \
           f'{data["subCategory"]} {name}\n\n' \
           f'{data["size"]}\n\n' \
           f'{data["price"]}\n\n' \
           f'За покупкой {userMention}'


def createMediaGroupForPost(clothInfo: dict):
    media = types.MediaGroup()
    for i in range(len(clothInfo['photo'])):
        media.attach_photo(photo=types.InputMediaPhoto(clothInfo['photo'][i],
                                                       caption=getClothInfoForChannel(clothInfo) if i == 0 else '',
                                                       parse_mode=types.ParseMode.HTML))
    return media


def chooseStatShowPeriod():
    return 'Выберите за какой период хотите посмотреть статистику'


def writeStatShowDay():
    return f'Напиши день за который хочешь просмотреть статистику в формате \n\n' \
           f'YYYY-MM-DD\n' \
           f'Например, {date.today()}'


rolesRules = {
    'can_delete_all': '🚫 Может удалять любые вещи\n',
    'access_statistics': '📈 Смотреть статистику бота\n',
    'can_post_in_group': '📝 Постить свои вещи в основную группу\n',
    'can_edit_roles': '👑 Изменять права других участников\n',
    'access_admin_panel': '😎 Доступ к панели админа\n',
    'can_add_clothes': '👕 Добавлять свои вещи\n',
    'access_catalog': '📲 Доступ к каталогу вещей\n'
}


def roleDescription(roles):
    text = 'Что могут разные роли\n\n'
    for role in roles:
        text += f'*{role["name"].upper()}\n*'
        for perm in rolesRules:
            if role[perm]:
                text += f'{rolesRules.get(perm, "")}'
    bannedPermissions = 'Ничего :('
    return text + bannedPermissions


def listOfUsersExceptRole(roleNameChangeTo, usersExceptRole):
    text = 'Список пользователей:\n'
    for user in usersExceptRole:
        text += f'/{user.telegram_id} - {user.mention}\n'
    text += f'Нажмите на айди пользователя чтобы изменить его роль на {roleNameChangeTo}'
    return text


def isActuallyChangeRoleToUser(roleNameChangeTo, userToChange):
    return f'Действительно изменить роль {userToChange.mention} на {roleNameChangeTo}?'