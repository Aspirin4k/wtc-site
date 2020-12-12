import re
from peewee import *

database = SqliteDatabase('db.sqlite')

class BaseModel(Model):
    class Meta:
        database = database

class Post(BaseModel):
    id = AutoField(unique=True)
    date = DateField()
    owner_id = IntegerField()
    vk_id = IntegerField()
    title = CharField()
    text = TextField()

    
class Tags(BaseModel):
    """Model that represent tags system."""
    id = AutoField(unique=True)
    vk_id = ForeignKeyField(Post, backref='tags')
    name = CharField()

    
class Attachments(BaseModel):
    id = AutoField(unique=True)
    vk_id = ForeignKeyField(Post, backref='attachments')
    type = CharField()
    url = CharField()
