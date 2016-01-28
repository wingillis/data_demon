from peewee import *

db = SqliteDatabase('demon_database.db')

class Base(Model):
    class Meta:
        database = db

class Job(Base):
    storeId = IntegerField()
    watchedFolder = CharField()
    fileFilter = CharField()
    outputPath = CharField()
    interval = CharField()
    # folder structure

def create_tables():
    db.create_tables([Job], safe=True)
