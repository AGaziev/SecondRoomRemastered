from model import *


def authorization(adminId):
    user = User.get(User.telegram_id == str(adminId))
    if user.role_id.access_admin_panel:
        return user.mention
    else:
        return False


def getAdminList():
    return User.select().where(User.role_id == 'admin').objects()


def canPostInGroup(id):
    return User.get(User.telegram_id == id).role_id.can_post_in_group