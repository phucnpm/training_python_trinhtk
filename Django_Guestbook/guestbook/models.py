from django.db import models
from google.appengine.ext import db
# Create your models here.
class Greeting(db.Model):
    #variables
    author = db.StringProperty()
    content = db.StringProperty(multiline=True)
    date = db.DateTimeProperty(auto_now_add=True)
    @classmethod
    def get_key_from_name(cls, guestbook_name):
        return db.Key.from_path('Guestbook', guestbook_name or 'default_guestbook')
