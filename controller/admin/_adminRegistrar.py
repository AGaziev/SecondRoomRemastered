from .adminPanel import *
from .addCloth import *
from controller.other._FSMOther import FSMOther
from model.cloth.categoriesInfo import getInfoAboutCategories


def registerHandlers(dp):
    dp.register_callback_query_handler(adminPanel, state=FSMOther.mainMenu, text='adminPanel')
    dp.register_message_handler(adminPanel, state='*', commands=['admin'])
    dp.register_callback_query_handler(backToLogin, state=FSMAdmin.panel, text='back')
    # add cloth
    dp.register_callback_query_handler(startAdding, state=FSMAdmin.panel, text='addCloth')
    dp.register_callback_query_handler(chooseSubCategory, state=FSMAdmin.category,
                                       text=getInfoAboutCategories().keys())
    dp.register_callback_query_handler(chooseBrand, state=FSMAdmin.subCategory)
    dp.register_message_handler(chooseBrand, state=FSMAdmin.subCategory)
    dp.register_message_handler(chooseName, state=FSMAdmin.brand)
    dp.register_message_handler(choosePrice, state=FSMAdmin.name)
    dp.register_message_handler(chooseSize, state=FSMAdmin.price)
    dp.register_message_handler(chooseCondition, state=FSMAdmin.size)
    dp.register_message_handler(choosePhoto, state=FSMAdmin.condition)
    dp.register_message_handler(Text(equals='-'), state=FSMAdmin.photo)
    dp.register_message_handler(endAddingCloth, content_types=['photo'], state=FSMAdmin.photo)
    dp.register_callback_query_handler(returnToAdminPanel, state=FSMAdmin.photo, text='returnToPanel')
