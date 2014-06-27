from google.appengine.ext import ndb
# Create your models here.
DEFAULT_NAME = 'default_guestbook'
class Greeting(ndb.Model):
    #variables
    author = ndb.StringProperty()
    content = ndb.StringProperty()
    date = ndb.DateTimeProperty(auto_now_add=True)

class Guestbook(ndb.Model):
    name = ndb.StringProperty()

    def get_key(self):
        return ndb.Key(Guestbook, self.name or self.get_default_name())
    def get_latest(self, count):
        return Greeting.query(
                    ancestor= self.get_key()).order(-Greeting.date).fetch(count)
    def put_greeting(self, author, content):
        greeting = Greeting(parent=self.get_key(), author= author, content= content)
        return greeting
    @classmethod
    def get_default_name(cls):
        return DEFAULT_NAME