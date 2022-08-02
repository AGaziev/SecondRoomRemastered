from config import DATABASE_PATH
from peewee import SqliteDatabase
import logging

try:
    db = SqliteDatabase(DATABASE_PATH)
except Exception as e:
    logging.critical(e)
