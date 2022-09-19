from model import *
from datetime import date
from model import DoesNotExist
from model.cloth.categoriesInfo import getInfoAboutSubcategories

def incrStatBySubcategory(subcategoryToIncr):
    today = date.today()
    try:
        sub = Subcategory.get(Subcategory.title == subcategoryToIncr)
    except Exception as e:
        return False
    statToIncr, created = Statistic.get_or_create(
        category=sub.of_category,
        subcategory=sub.id,
        date=today)
    statToIncr.incr().save()
    return True
