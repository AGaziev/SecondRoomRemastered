from model import *


def authorization(adminId):
    print(adminId, type(adminId))
    user = User.get(User.telegram_id == str(adminId))
    if user.role_id.acces_admin_panel:
        return user.mention
    else:
        return False

def getAdminList():
    return User.select().where(User.role_id == 'admin').objects()