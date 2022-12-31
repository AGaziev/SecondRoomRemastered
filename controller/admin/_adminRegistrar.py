from .adminPanel import *
from .addCloth import *
from .statisticShow import *
from .userRoleControl import *
from controller.other._FSMOther import FSMOther
from model.cloth.categoriesInfo import getInfoAboutCategories
from model.roles.rolesControl import getRoleNames
from aiogram import filters


def registerHandlers(dp):
    dp.register_callback_query_handler(adminPanel, state=FSMOther.mainMenu, text='adminPanel')
    dp.register_message_handler(adminPanel, state='*', commands=['admin'])
    dp.register_callback_query_handler(postDelayed, state=FSMAdmin.panel, text='postDelayed')
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
    dp.register_message_handler(deleteLastPhoto,Text(equals='-'), state=FSMAdmin.photo)
    dp.register_message_handler(endAddingCloth, content_types=['photo'], state=FSMAdmin.photo)
    dp.register_callback_query_handler(returnToAdminPanel, state=FSMAdmin.confirmationPostingInGroup, text='no')
    dp.register_callback_query_handler(postingInGroup, state=FSMAdmin.confirmationPostingInGroup, text='yes')
    dp.register_callback_query_handler(delayPostingInGroup, state=FSMAdmin.confirmationPostingInGroup, text='delay')
    dp.register_callback_query_handler(confirmationOfPosting, state=FSMAdmin.photo, text='endAddingCloth')
    #statistics
    dp.register_callback_query_handler(statisticChoose, state=FSMAdmin.panel, text='statistics')
    dp.register_callback_query_handler(statisticDayWrite, state=FSMAdmin.statChoose, text='day')
    dp.register_message_handler(statisticDayShow, state=[FSMAdmin.statDay, FSMAdmin.statWriteDay],
                                regexp=r'(?P<year>20\d{2})[\.\-\/\\](?P<month>\d{2})[\.\-\/\\](?P<day>\d{2})')
    dp.register_callback_query_handler(statisticWeekShow, state=FSMAdmin.statChoose, text='lastWeek')
    #roles
    dp.register_callback_query_handler(chooseRoleChangeTo, state=FSMAdmin.panel, text='editRoles')
    dp.register_callback_query_handler(chooseUser, state=FSMAdmin.chooseRoleChangeTo, text=getRoleNames())
    dp.register_message_handler(confirmationOfChanging, state=FSMAdmin.writeID, regexp=r'/\d+')
    dp.register_callback_query_handler(returnToChoosing, state=FSMAdmin.confirmationRoleChanging, text='no')
    dp.register_callback_query_handler(changingRoleAndReturn, state=FSMAdmin.confirmationRoleChanging, text='yes')