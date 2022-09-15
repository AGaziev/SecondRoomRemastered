from config import DATABASE_PATH
from peewee import SqliteDatabase
import logging

try:
    db = SqliteDatabase(DATABASE_PATH, pragmas={'foreign_keys': 1})
except Exception as e:
    logging.critical(e)
