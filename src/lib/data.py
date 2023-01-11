"""Module for data ORM with MongoDB"""
import os
from mongoengine import connect, StringField, DateField, DateTimeField, Document


client = connect(host=os.getenv('DATABASE_URI', 'mongodb://localhost'))


class Notice(Document):
    """ORM for 'notices' collection in mongodb"""
    title = StringField(required=True)
    subtitle = StringField(required=True)
    image = StringField(required=True)
    content = StringField(required=True)
    url = StringField(required=True)
    date = DateField()
    createdAt = DateTimeField()
    updatedAt = DateTimeField()
