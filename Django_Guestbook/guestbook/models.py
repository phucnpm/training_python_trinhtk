from google.appengine.ext import ndb
# Create your models here.
class Greeting(ndb.Model):
    #variables
    author = ndb.StringProperty()
    content = ndb.StringProperty()
    date = ndb.DateTimeProperty(auto_now_add=True)
    @classmethod
    def get_key_from_name(cls, guestbook_name):

        return ndb.Key('Guestbook', guestbook_name or 'default_guestbook')
    def Update_Info(self, content, author ):
        self.author = author
        self.content = content