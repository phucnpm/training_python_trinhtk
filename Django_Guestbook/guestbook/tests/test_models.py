import logging
from google.appengine.ext import db
from google.appengine.ext import testbed
from google.appengine.ext import ndb
from google.appengine.ext.ndb.key import Key
import pytest
import unittest
from guestbook.models import Greeting, Guestbook
import guestbook

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

    def test_greeting_get_page(self):
        guestbook_name = "default_guestbook"
        curs = None
        pagesize = 10
        myGuestbook = Guestbook(name=guestbook_name)
        assert Greeting.get_page(guestbook_name, pagesize, curs) == Greeting.query(
                    ancestor= ndb.Key(Guestbook, guestbook_name)).order(-Greeting.date).fetch_page(pagesize, start_cursor=curs)

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

    def test_guestbook_get_key(self):
        self.guestbook_name = "default_guestbook"
        myGuestbook = Guestbook(name=self.guestbook_name)
        assert myGuestbook.get_key() == ndb.Key("Guestbook", self.guestbook_name)

if __name__ == '__main__':
    unittest.main()