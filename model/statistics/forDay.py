import peewee

from model import *
from config import GRAPH_SRC_PATH

import matplotlib.pyplot as plt
import datetime
import re
import numpy as np


def getStatsPictPathPerDay(rawDate):
    dateRegular = r'(?P<year>20\d{2})[\.\-\/\\](?P<month>\d{2})[\.\-\/\\](?P<day>\d{2})'
    dateAttributes = re.match(dateRegular, rawDate).groups()
    day = datetime.date(*map(int, dateAttributes))
    getPlotCategoriesStats(day)
    getPlotSubcategoriesStats(day)
    plt.tight_layout()
    savePath = f'{GRAPH_SRC_PATH}/statsFor({rawDate}).png'
    plt.savefig(savePath)
    plt.clf()
    return savePath


def getPlotCategoriesStats(date):
    info = Statistic.select(Category.title.alias('categoryName'), fn.SUM(Statistic.count)) \
        .join(Category) \
        .where(Statistic.date == date) \
        .group_by(Statistic.category).dicts()

    catsX = np.array([i['categoryName'] for i in info])
    countsY = np.array([i['count'] for i in info])

    plt.subplot(3, 2, 3)
    return plt.pie(countsY,
                   labels=catsX,
                   shadow=True,
                   autopct=makeAutopct(countsY),
                   radius=1.9,
                   pctdistance=0.7)


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
        plt.subplot(3, 2, (id + 1) * 2)
        plt.xticks(range(min(subcatStatsCounters), max(subcatStatsCounters) + 1))
        subPlot = plt.barh(subcatNames,
                           subcatStatsCounters
                           )
        plotsForSubcategories.append(subPlot)
    return plotsForSubcategories


def makeAutopct(values):  # thx stackoverflow
    def my_autopct(pct):
        total = sum(values)
        val = int(round(pct * total / 100.0))
        return '{v:d}'.format(p=pct, v=val)

    return my_autopct