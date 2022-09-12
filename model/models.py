from peewee import *
from repositories import db
import datetime


class BaseModel(Model):
    id = PrimaryKeyField(unique=True)

    class Meta:
        database = db
        order_by = 'id'


class Category(BaseModel):
    title = CharField()

    class Meta:
        db_table = 'Category'


class Subcategory(BaseModel):
    title = CharField()
    of_category = ForeignKeyField(Category)

    class Meta:
        db_table = 'Subcategory'


class Role(Model):
    name = CharField(primary_key=True)
    can_post_in_group = BooleanField()
    access_admin_panel = BooleanField()
    access_statistics = BooleanField()
    access_catalog = BooleanField()
    can_delete_all = BooleanField()
    can_add_sellers = BooleanField()
    can_add_clothes = BooleanField()

    class Meta:
        database = db
        db_table = 'Role'


class User(Model):
    telegram_id = CharField(primary_key=True, unique=True)
    first_name = CharField(null=True)
    last_name = CharField(null=True)
    username = CharField(null=True)
    role_id = ForeignKeyField(Role)
    date_of_registration = DateField(default=datetime.date.today())

    @property
    def full_name(self):
        """
        You can get full name of user.

        :return: str
        """
        full_name = self.first_name
        if self.last_name != 'None':
            full_name += ' ' + self.last_name
        return full_name

    @property
    def mention(self):
        """
        You can get user's username to mention him
        Full name will be returned if user has no username

        :return: str
        """
        if self.username != 'None':
            return '@' + self.username
        return self.full_name

    class Meta:
        database = db
        db_table = 'User'


class Cloth(BaseModel):
    brand = CharField(null=True)
    condition = CharField()
    cloth_name = CharField(null=True)
    price = CharField(null=True, default='FREE')
    size = CharField()
    subcategory = ForeignKeyField(Subcategory)
    category = ForeignKeyField(Category)
    seller = ForeignKeyField(User)
    timestamp = DateTimeField(default=[SQL('DEFAULT CURRENT_TIMESTAMP')])

    class Meta:
        db_table = 'Cloth'


class Photo(BaseModel):
    photoId = CharField()
    of_cloth = ForeignKeyField(Cloth)

    class Meta:
        db_table = 'Photo'


class NoveltyInfo(Model):
    user = ForeignKeyField(User)
    subcategory = ForeignKeyField(Subcategory)
    category = ForeignKeyField(Category)

    class Meta:
        database = db
        indexes = (
            (('user', 'subcategory', 'category'), True),
        )
        db_table = 'NoveltyInfo'

class Statistic(BaseModel):
    category = ForeignKeyField(Category)
    subcategory = ForeignKeyField(Subcategory)
    count = IntegerField(null=True,default=0)
    date = DateField(null=True,default=[SQL('DEFAULT CURRENT_DATE')])

    class Meta:
        db_table = 'Statistic'