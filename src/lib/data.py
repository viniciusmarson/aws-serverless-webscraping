"""Module for data ORM with MongoDB"""
import os
from mongoengine import connect, StringField, DateField, DateTimeField, Document


client = connect(host=os.getenv('MONGO_URI', 'mongodb://localhost'))


class Notice(Document):
    """ORM for 'notices' collection in mongodb"""
    url = StringField(required=True)
    title = StringField(required=True)
    subtitle = StringField()
    image = StringField()
    content = StringField()
    date = DateField()
    createdAt = DateTimeField()
    updatedAt = DateTimeField()
