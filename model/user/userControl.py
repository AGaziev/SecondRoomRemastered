from model import *
from playhouse.shortcuts import model_to_dict
from model.novelty.noveltyControl import addNoveltyForNewUser


def isUserRegistered(id):
    if getUserById(id):
        return True
    else:
        return False


def getUserById(id):
    for result in User.select().where(User.telegram_id == id).limit(1).objects():
        return result


def registerUser(userInfoFromMessage):
    userInfo = userInfoFromMessage.copy()  # preventing corruption of information in message
    userInfo['telegram_id'] = str(userInfo.pop('id'))
    userInfo['role_id'] = 'client'
    user = User.create(**userInfo)
    user.save()
    addNoveltyForNewUser(user)
    return user


def getUserRole(user):
    return model_to_dict(user.role_id)


def getUserListExceptRole(roleName):
    return User.select().where(User.role_id != roleName)


def changeUserRole(id, roleName):
    try:
        user = getUserById(id)
        user.role_id = Role.get(Role.name == roleName)
        user.save()
    except Exception:
        return
