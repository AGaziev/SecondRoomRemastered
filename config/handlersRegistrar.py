from controller.other._otherRegistrar import registerHandlers as otherRegistrar
from controller.client._clientRegistrar import registerHandlers as clientRegistrar

def registerAll(dp):
    otherRegistrar(dp)
    clientRegistrar(dp)
