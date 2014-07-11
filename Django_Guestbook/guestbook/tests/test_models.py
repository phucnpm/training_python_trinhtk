import logging
from google.appengine.api import memcache
from google.appengine.ext import testbed
from google.appengine.ext import ndb
import unittest
from guestbook.models import Greeting, Guestbook
from mock import MagicMock, Mock


class MyFirstTest(unittest.TestCase):

    def setUp(self):
        self.testbed = testbed.Testbed()
        # Then activate the testbed, which prepares the service stubs for use.
        self.testbed.activate()
        # Next, declare which service stubs you want to use.
        self.testbed.init_datastore_v3_stub()
        self.testbed.init_memcache_stub()
        self.testbed.init_user_stub()

        # create test DB
        self.guestbook_name = 'default_guestbook'
        myGuestbook = Guestbook(name=self.guestbook_name)
        i = 0
        while i < 19:
            key = Greeting(parent=myGuestbook.get_key(),author="Author test %s" %i, content='Content test %s' %i).put()
            i +=1

    def tearDown(self):
      self.testbed.deactivate()

    #test function Greeting.get_page(cls, guestbook_name, pagesize, cursor=None):
    def test_greeting_get_page(self):
        guestbook_name = "default_guestbook"
        curs = None
        pagesize = 10
        myGuestbook = Guestbook(name=guestbook_name)
        assert Greeting.get_page(guestbook_name, pagesize, curs) == Greeting.query(
                    ancestor= ndb.Key(Guestbook, guestbook_name)).order(-Greeting.date).fetch_page(pagesize, start_cursor=curs)

    #test function Greeting.greeting_to_dict(self):
    def test_greeting_to_dict(self):
        greeting = Greeting.query(Greeting.content == "Content test 1", Greeting.author=="Author test 1").fetch(1)[0]
        id = greeting.key.id()
        guestbook_name = "default_guestbook"
        myGuestbook = Guestbook(name=guestbook_name)
        myGreeting = myGuestbook.get_greeting_by_id(id)
        dict = {}
        dict["author"] = "Author test 1"
        dict['content'] = "Content test 1"
        dict['last udated by'] = None
        dict['pub date'] = myGreeting.date.strftime("%Y-%m-%d %H:%M +0000")
        dict['date modified'] = None
        assert dict == myGreeting.greeting_to_dict()

    #test function Guestbook.get_key(self):
    def test_guestbook_get_key(self):
        self.guestbook_name = "default_guestbook"
        myGuestbook = Guestbook(name=self.guestbook_name)
        assert myGuestbook.get_key() == ndb.Key("Guestbook", self.guestbook_name)

    #test function Guestbook.get_latest(self, count):
    def test_guestbook_get_latest(self):
        self.guestbook_name = "default_guestbook"
        count = 10
        myGuestbook= Guestbook(name=self.guestbook_name)
        listGreeting = Greeting.query(
                    ancestor= myGuestbook.get_key()).order(-Greeting.date).fetch(count)
        assert listGreeting == myGuestbook.get_latest(count)

    #test function Guestbook.delete_greeting(self, id):
    def test_guestbook_delete_greeting(self):
        self.guestbook_name = "default_guestbook"
        myGuestbook = Guestbook(name= self.guestbook_name)
        #delete id = 1
        id = 1
        myGuestbook.delete_greeting(id)
        assert None == myGuestbook.get_greeting_by_id(id)

    #test function Guestbook.get_greeting_by_id(self, id):
    def test_guestbook_get_greeting_by_id(self):
        self.guestbook_name = "default_guestbook"
        myGuestbook = Guestbook(name= self.guestbook_name)
        #get greeting where id = 2
        id = 2
        greeting_man = myGuestbook.get_greeting_by_id(id)
        greeting_func = ndb.Key(Guestbook, self.guestbook_name, Greeting, int(id)).get()
        assert greeting_man == greeting_func

    #test function Guestbook.get_default_name(cls):
    def test_guestbook_get_default_name(self):
        assert "default_guestbook" == Guestbook.get_default_name()

    #test function Guestbook.put_greeting(self, author, content):
    # def test_function_put_greeting(self):
    #
if __name__ == '__main__':
    unittest.main()