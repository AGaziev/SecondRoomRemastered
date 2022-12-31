from model import *
from model.user.userControl import getUserById


def addDelayedCloth(clothId, userId):
    info = PendingCloth(cloth=clothId, seller=userId)
    info.save()


def getDelayedClothsForSeller(userId):
    mention = getUserById(userId).mention
    cloths = PendingCloth.select(Cloth.cloth_name.alias('name'),
                                 Cloth.brand,
                                 Cloth.size,
                                 Cloth.price,
                                 Cloth.id.alias('clothId'),
                                 Subcategory.title.alias('subCategory'),
                                 PendingCloth.seller.alias('userId'),
                                 SQL(f"\"{mention}\" as user"), ). \
        join(Cloth, on=PendingCloth.cloth == Cloth.id). \
        join(Subcategory, on=Cloth.subcategory == Subcategory.id). \
        where(PendingCloth.seller == userId).dicts()
    for cloth in cloths:
        photos = Photo.select(Photo.photoId).where(Photo.of_cloth == cloth['clothId'])
        cloth['photo'] = [p.photoId for p in photos]
    return cloths


def deletePostedCloths(cloths: list):
    query = PendingCloth.delete().where(PendingCloth.cloth << [cloth['clothId'] for cloth in cloths])
    query.execute()
