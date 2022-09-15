import peewee

from model import *

import matplotlib.pyplot as plt
import datetime
import re
import numpy as np
import pandas as pd


def getStatsPictPerDay(rawDate):
    dateRegular = r'(?P<year>20\d{2})[\.\-\/\\](?P<month>\d{2})[\.\-\/\\](?P<day>\d{2})'
    dateAttributes = re.match(dateRegular, rawDate).groups()
    day = datetime.date(*map(int, dateAttributes))
    plt.subplots(2,2, figsize=(10,10))
    categoriesPlot = getPlotCategoriesStats(day)
    subcategoriesPlots = getPlotSubcategoriesStats(day)
    plt.show()


def getPlotCategoriesStats(date):
    info = Statistic.select(Category.title.alias('categoryName'), fn.SUM(Statistic.count)) \
        .join(Category) \
        .where(Statistic.date == date) \
        .group_by(Statistic.category).dicts()

    catsX = np.array([i['categoryName'] for i in info])
    countsY = np.array([i['count'] for i in info])

    plt.subplot(2,2,1)
    plt.title('Количество вхождение в каждую из категорий')
    return plt.pie(countsY,
                   labels=catsX,
                   shadow=True,
                   autopct=make_autopct(countsY),
                   radius=2,
                   textprops={'fontsize': 10})


def getPlotSubcategoriesStats(date):
    info = Statistic.select(Subcategory.title.alias('subcategoryName'),
                            Category.title.alias('categoryName'),
                            Statistic.count) \
        .join(Subcategory) \
        .join(Category) \
        .where(Statistic.date == date).dicts()
    data = {}
    categoriesWithStats = set()
    for i in info:
        data.setdefault(i['categoryName'], {i['subcategoryName']: i['count']}).update(
            {i['subcategoryName']: i['count']})
        categoriesWithStats.add(i['categoryName'])
    plotsForSubcategories = []
    for id, subcatStatsInfo in enumerate(data.values()):
        subcatNames = list(subcatStatsInfo.keys())
        subcatStatsCounters = list(subcatStatsInfo.values())
        plt.subplot(2,2,id+2)
        subPlot = plt.barh(subcatNames, subcatStatsCounters, height=0.5)
        plotsForSubcategories.append(subPlot)
    return plotsForSubcategories

def make_autopct(values):  # thx stackoverflow
    def my_autopct(pct):
        total = sum(values)
        val = int(round(pct * total / 100.0))
        return '{p:.2f}%  ({v:d})'.format(p=pct, v=val)

    return my_autopct


getStatsPictPerDay('2022-09-15')
