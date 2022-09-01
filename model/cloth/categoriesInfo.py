import logging
from model import *


def getCategories():
    with db:
        subInfo = Subcategory.select(Subcategory.title.alias('sub'),
                                     Category.title.alias('cat'),
                                     Category.id.alias('category_id'),
                                     Subcategory.id.alias('subcategory_id'),
                                     fn.Count(Cloth.id != 'None').alias('c')) \
            .join(Category) \
            .left_outer_join(Cloth, on=Cloth.subcategory == Subcategory.id).group_by(Subcategory.id).dicts()
    return subInfo


def getInfoAboutSubcategories():
    subInfo = getCategories()
    categoryList = {k.title: {} for k in Category.select(Category.title)}
    for i in subInfo:
        categoryList[i['cat']].update({i['sub']: i['c']})
    return categoryList

def getInfoAboutCategories() -> dict:
    categoriesInfo = {}
    for category, subsInfo in getInfoAboutSubcategories().items():
        categoriesInfo[category] = sum(subsInfo.values())
    return categoriesInfo


def getNumberOfClothes(category, subCategory) -> int:
    return getInfoAboutSubcategories()[category][subCategory]


def categoriesWithNew(id):  # get categories with new items
    userId = str(id)
    categoriesWithNew = Category.select(Category.title) \
        .where(Category.id.in_(NoveltyInfo.select(NoveltyInfo.category)
                               .where(NoveltyInfo.user_id == userId)))
    return [category.title for category in categoriesWithNew]


def subcatWithNew(id):  # get subcategories with new items
    userId = str(id)
    subcategoriesWithNew = Subcategory.select(Subcategory.title) \
        .where(Subcategory.id.in_(NoveltyInfo.select(NoveltyInfo.subcategory)
                                  .where(NoveltyInfo.user_id == userId)))
    return [subCategory.title for subCategory in subcategoriesWithNew]


print(getInfoAboutCategories().keys())