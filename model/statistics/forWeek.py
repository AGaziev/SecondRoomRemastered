from model import *
from config import GRAPH_SRC_PATH

import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
import datetime
import numpy as np
from model.cloth.categoriesInfo import getCategories


def getStatsPictPathPerWeek():
    weekAgo = datetime.date.today() - datetime.timedelta(days=7)
    getPlotCategoriesStats(weekAgo)
    getPlotUserRegistrationsStats(weekAgo)
    plt.tight_layout()
    savePath = f'{GRAPH_SRC_PATH}/statsForWeek({weekAgo}_by_{datetime.date.today()}).png'
    plt.savefig(savePath)
    plt.clf()
    return savePath


def getPlotCategoriesStats(weekAgo):
    info = Statistic.select(fn.SUM(Statistic.count), Statistic.date, Statistic.category) \
        .join(Category) \
        .where(Statistic.date.between(weekAgo, datetime.date.today())) \
        .group_by(Statistic.category, Statistic.date).dicts()

    plotsForCategoriesPerWeek = []
    datesList = [datetime.date.today() - datetime.timedelta(days=x) for x in range(7)][::-1]

    structuredInfo = {}
    for record in info:
        structuredInfo.setdefault(record['date'], {}).update({record['category']: record['count']})

    for index, cat in enumerate(getCategories().group_by(Subcategory.of_category)):
        daysX = np.array([f"{i.day}.{i.month}" for i in datesList])
        countsY = np.array([structuredInfo[i].get(cat['category_id'], 0)
                            if i in structuredInfo.keys() else 0 for i in datesList])
        plt.subplot(2, 2, index + 1)
        plt.gca().yaxis.set_major_locator(MaxNLocator(integer=True))
        plt.title(f'Вхождения в категорию {cat["cat"]}', fontdict={'fontsize': 10})
        plotsForCategoriesPerWeek.append(plt.plot(daysX, countsY, 'bo-'))
        plt.fill_between(daysX, countsY)
    return plotsForCategoriesPerWeek


def getPlotUserRegistrationsStats(weekAgo):
    info = User.select(fn.COUNT().alias('count'), User.date_of_registration) \
        .where(User.date_of_registration.between(weekAgo, datetime.date.today())) \
        .group_by(User.date_of_registration).dicts()

    datesList = [datetime.date.today() - datetime.timedelta(days=x) for x in range(7)][::-1]

    structuredInfo = {}
    for record in info:
        structuredInfo[record['date_of_registration']] = record['count']

    daysX = np.array([f"{i.day}.{i.month}" for i in datesList])
    countsY = np.array([structuredInfo[i] if i in structuredInfo.keys() else 0 for i in datesList])
    plt.subplot(2, 2, 4)
    plt.gca().yaxis.set_major_locator(MaxNLocator(integer=True))
    plt.title(f'Количество регистраций', fontdict={'fontsize': 10})
    plt.plot(daysX, countsY, 'bo-')
    plt.fill_between(daysX, countsY)

getStatsPictPathPerWeek()
