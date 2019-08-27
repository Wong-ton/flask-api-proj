from peewee import *
from flask_login import UserMixin
from playhouse.db_url import connect
import datetime
import os

# TEST DB
DATABASE = SqliteDatabase('flicks.sqlite')
# Heroku DB
# DATABASE = connect(os.environ.get('DATABASE_URL'))

class User(UserMixin, Model):
    name = CharField(unique=True)
    email = CharField(unique=True)
    password = CharField(unique=True)

    class Meta:
        database = DATABASE

class Flick(Model):
    title = CharField() # Movie Title
    name = CharField() # Show Name
    poster_path = CharField()
    overview = CharField()
    user = ForeignKeyField(User, backref='flick')

    class Meta:
        database = DATABASE

def initialize():
    DATABASE.connect()
    DATABASE.create_tables([User, Flick], safe=True)
    print("TABLES CREATED.")
    DATABASE.close()