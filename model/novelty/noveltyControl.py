from model.cloth import categoriesInfo
from model.models import *


def setNoveltyToUsers(subCategory, novelty):
    listOfUsersId = User.select(User.telegram_id)
    subCategoryModel = Subcategory.get(Subcategory.title == subCategory)
    categoryId = subCategoryModel.of_category.id
    noveltyInfoList = []
    if novelty:
        for userId in listOfUsersId:
            n, created = NoveltyInfo.get_or_create(user_id=userId.telegram_id,
                                      subcategory_id=subCategoryModel.id,
                                      category_id=categoryId)
            n.save()
    else:
        NoveltyInfo.delete().where(NoveltyInfo.category == categoryId,
                                   NoveltyInfo.subcategory == subCategoryModel.id).execute()


def notNewAnymore(id, category, subCategory):  # falsing new for subcategory
    subCategoryModel = Subcategory.get(Subcategory.title == subCategory)
    categoryId = subCategoryModel.of_category.id
    NoveltyInfo.delete().where(NoveltyInfo.user_id == id,
                               NoveltyInfo.category == categoryId,
                               NoveltyInfo.subcategory == subCategoryModel.id).execute()


def listForNewUser(userId):  # get list for new users depended on clothes counters (false if no cloth in subcategory
    noveltyListForNewUser = []
    userId = User.get(User.telegram_id == userId)
    for row in categoriesInfo.getCategories():
        if int(row['c']) > 0:
            noveltyListForNewUser.append({'user_id': userId,
                                          'subcategory_id': row['subcategory_id'],
                                          'category_id': row['category_id']})
    return noveltyListForNewUser


def addNoveltyForNewUser(userId):
    NoveltyInfo.insert_many(listForNewUser(userId),
                            fields=[NoveltyInfo.user,
                                    NoveltyInfo.subcategory,
                                    NoveltyInfo.category]) \
        .execute()
