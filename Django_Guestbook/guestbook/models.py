import datetime
from google.appengine.api import memcache
from google.appengine.ext import ndb
from google.appengine.api import users
try:
    from google.appengine.api.labs import taskqueue
except ImportError:
    from google.appengine.api import taskqueue
# Create your models here.
DEFAULT_NAME = 'default_guestbook'
class Greeting(ndb.Model):
    #variables
    author = ndb.StringProperty()
    content = ndb.StringProperty()
    date = ndb.DateTimeProperty(auto_now_add=True)
    last_update = ndb.DateTimeProperty()
    updated_by = ndb.StringProperty()
    def delete(self):
        query = Greeting.query(Greeting.date == self.date, Greeting.author == self.author, Greeting.content == self.content).fetch(1, keys_only=True)
        ndb.delete_multi(query)
class Guestbook(ndb.Model):
    name = ndb.StringProperty()
    def get_key(self):
        return ndb.Key(Guestbook, self.name or self.get_default_name())
    def get_latest(self, count):
        return Greeting.query(
                    ancestor= self.get_key()).order(-Greeting.date).fetch(count)
    @ndb.transactional
    def put_greeting(self, author, content):
        greeting = Greeting(parent=self.get_key(), author= author, content= content)
        if greeting.put():
            if users.get_current_user():
                taskqueue.add(url='/send/',method='GET', params={'guestbook_name':self.name, 'author':users.get_current_user().nickname(), 'content':content})
            else:
                taskqueue.add(url='/send/',method='GET', params={'guestbook_name':self.name, 'author': None, 'content':content})
            memcache.delete("%s:greetings" %self.name)
    @ndb.transactional
    def delete_greeting(self, id):
        key = ndb.Key(Guestbook, self.name, Greeting, int(id))
        key.delete()
        memcache.delete("%s:greetings" %self.name)
    @ndb.transactional
    def update_greeting(self, id, content, user):
        key = ndb.Key(Guestbook, self.name, Greeting, int(id))
        myGreeting = key.get()
        myGreeting.content = content
        myGreeting.updated_by = user
        myGreeting.last_update = datetime.datetime.now()
        if myGreeting.put():
            memcache.delete("%s:greetings" %self.name)
    @ndb.transactional
    def get_greeting_by_id(self, id):
        return ndb.Key(Guestbook, self.name, Greeting, int(id)).get()
    @classmethod
    def get_default_name(cls):
        return DEFAULT_NAME
