import logging

import datetime
from model import *
from model.novelty import noveltyControl
from .categoriesInfo import getNumberOfClothes

showInfo = ['subCategory', 'brand', 'name', 'price', 'condition', 'photo', 'size', 'user', 'userId', 'date']


def addClothToDB(data):
    logging.info(
        f'Adding new cloth in base {data["category"]},{data["subCategory"]} with name: {data["brand"]} \"{data["name"]}\"')

    with db:
        clothData = Cloth(**data)  # brand, condition, size, price
        # seller id
        clothData.seller_id = data['userId']
        # name
        clothData.cloth_name = data.get('name')
        # timestamp
        dateInfo = data.get('date', '2022-01-01')
        date = list(map(int, dateInfo.split('-')))
        clothData.timestamp = datetime.datetime(*date)
        # subcat, cat
        catId = Subcategory.get(Subcategory.title == data['subCategory']).of_category
        subcatId = Subcategory.get(Subcategory.title == data['subCategory']).id
        clothData.category = catId
        clothData.subcategory = subcatId
        #saving
        clothData.save()
        # photo
        for photoId in data['photo']:
            Photo.create(photoId=photoId, of_cloth_id=clothData.id)

    noveltyControl.setNoveltyToUsers(data['subCategory'], True)


def deleteClothFromDB(category, subCategory, clothId):
    logging.info(
        f'Deleting cloth from base {category}, {subCategory} with id: {clothId}')
    with db:
        Cloth.delete().where(Cloth.id == clothId).execute()
        Photo.delete().where(Photo.of_cloth == clothId).execute()
    count = getNumberOfClothes(category, subCategory)
    if count == 0:
        noveltyControl.setNoveltyToUsers(subCategory, False)


def getClothesList(category, subCategory):
    clothesList = Cloth.select(Cloth.id,
                               Cloth.brand,
                               Cloth.condition,
                               Cloth.cloth_name.alias('name'),
                               Cloth.price,
                               Cloth.size,
                               Cloth.timestamp.alias('date'),
                               User.telegram_id.alias('userId'),
                               Subcategory.title.alias('subCategory'),
                               Category.title.alias('category')) \
        .left_outer_join(Category, on=Cloth.category == Category.id) \
        .left_outer_join(Subcategory, on=Cloth.subcategory == Subcategory.id) \
        .left_outer_join(User, on=Cloth.seller == User.telegram_id) \
        .where(Category.title == category and Subcategory.title == subCategory).dicts()
    for cloth in clothesList:
        photos = Photo.select(Photo.photoId).where(Photo.of_cloth == cloth['id'])
        cloth['photo'] = [p.photoId for p in photos]
    return list(clothesList)