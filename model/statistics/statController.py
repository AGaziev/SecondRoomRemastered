from model import *
from datetime import date
from model import DoesNotExist

def incrStatBySubcategory(subcategoryToIncr):
    today = date.today()
    try:
        sub = Subcategory.get(Subcategory.title == subcategoryToIncr)
    except Exception as e:
        return False
    try:
        statToIncr = Statistic.get(Statistic.date == today and Statistic.subcategory == sub)
    except DoesNotExist:
        statInfo = {
            'category': sub.of_category,
            'subcategory': sub.id,
            'date': today
        }
        statToIncr = Statistic.create(**statInfo)
        statToIncr.save()
    finally:
        statToIncr.incr().save()
    return True