from peewee import *
from create_bot import db


class History(Model):
    name_city = CharField(max_length=256)
    address = TextField()
    description = TextField()
    price = FloatField()
    rating = FloatField()

    class Meta:
        database = db
