from django.conf import settings
from mongoengine import connect

def connect_db():
    connect(host=getattr(settings, "MONGO_HOST"))