from config import DATABASE_PATH
from peewee import SqliteDatabase

db = SqliteDatabase(DATABASE_PATH)

