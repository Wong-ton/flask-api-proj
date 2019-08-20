from peewee import *
from flask_login import UserMixin
import datetime

# TEST DB
DATABASE = SqliteDatabase('movies.sqlite')

class User(UserMixin, Model):
    username = CharField(unique=True)
    email = CharField(unique=True)
    password CharField(unique=True)
    image = CharField()

    class Meta:
        database = DATABASE

class Flick(Model):
    name = CharField()
    genre = CharField()
    overview = CharField()

    class Meta:
        database = DATABASE

de initialize():
DATABASE.connect()
DATABASE.create_tables([User, Flick], safe=True)
print("TABLES CREATED.")
DATABASE.close()