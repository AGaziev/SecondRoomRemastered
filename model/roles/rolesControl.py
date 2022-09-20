from model import *

def getRoles():
    return Role.select().dicts()