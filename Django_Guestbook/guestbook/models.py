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

    def greeting_to_dict(self):

        dict = {}
        dict["author"] = self.author
        dict['content'] = self.content
        dict['last udated by'] = self.updated_by
        dict['pub date'] = self.date.strftime("%Y-%m-%d %H:%M +0000")
        if self.last_update:
            dict['date modified'] = self.last_update.strftime("%Y-%m-%d %H:%M +0000")
        else:
            dict['date modified'] = None
        return dict

    @classmethod
    def get_page(cls, guestbook_name, pagesize, cursor=None):

        items, nextcurs, more = Greeting.query(
                    ancestor= ndb.Key(Guestbook, guestbook_name)).order(-Greeting.date).fetch_page(pagesize, start_cursor=cursor)
        return items, nextcurs, more

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
