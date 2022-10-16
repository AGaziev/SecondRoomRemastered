from model import *


def getRoles():
    return Role.select().dicts()


def getRoleNames():
    roleNames = []
    for role in Role.select(Role.name):
        roleNames.append(role.name)
    return roleNames
