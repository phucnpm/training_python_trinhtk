from google.appengine.ext import ndb
# Create your models here.
class Greeting(ndb.Model):
    #variables
    author = ndb.StringProperty()
    content = ndb.StringProperty()
    date = ndb.DateTimeProperty(auto_now_add=True)


class Guestbook(ndb.Model):
    name = ndb.StringProperty()
    @classmethod
    def get_key(cls, name):
        return ndb.Key('Guestbook', name or 'default_guestbook')