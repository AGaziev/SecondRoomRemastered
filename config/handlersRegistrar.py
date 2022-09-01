from controller.other._otherRegistrar import registerHandlers as otherRegistrar
from controller.client._clientRegistrar import registerHandlers as clientRegistrar
from controller.admin._adminRegistrar import registerHandlers as adminRegistrar

def registerAll(dp):
    otherRegistrar(dp)
    clientRegistrar(dp)
    adminRegistrar(dp)