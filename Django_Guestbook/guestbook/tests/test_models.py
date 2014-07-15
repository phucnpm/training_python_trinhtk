import logging
from google.appengine.ext import testbed
from google.appengine.ext import ndb
import pytest
from guestbook.models import Greeting, Guestbook


class TestBaseClass():

    guestbook_name = "default_guestbook"
    myGuestbook = Guestbook(name=guestbook_name)


    def setup_method(self, method):

        self.testbed = testbed.Testbed()
        # Then activate the testbed, which prepares the service stubs for use.
        self.testbed.activate()
        # Next, declare which service stubs you want to use.
        self.testbed.init_datastore_v3_stub()
        self.testbed.init_memcache_stub()
        self.testbed.init_user_stub()
        # create test DB
        i = 0
        while i < 19:
            key = Greeting(parent=self.myGuestbook.get_key(),author="Author test %s" %i, content='Content test %s' %i).put()
            i +=1

    def teardown_method(self, method):

        self.testbed.deactivate()

#=======TEST FOR GREETING CLASS========
class TestGreeting(TestBaseClass):

    #test function Greeting.get_page(cls, guestbook_name, pagesize, cursor=None):
    def test_greeting_get_page(self):

        curs = None
        pagesize = 10
        assert Greeting.get_page(self.guestbook_name, pagesize, curs) == Greeting.query(
                    ancestor= ndb.Key(Guestbook, self.guestbook_name)).order(-Greeting.date).fetch_page(pagesize, start_cursor=curs)

    #test function Greeting.greeting_to_dict(self):
    def test_greeting_to_dict(self):

        greeting = Greeting.query(Greeting.content == "Content test 1", Greeting.author=="Author test 1").fetch(1)[0]
        id = greeting.key.id()
        myGreeting = self.myGuestbook.get_greeting_by_id(id)
        dict = {}
        dict["author"] = "Author test 1"
        dict['content'] = "Content test 1"
        dict['last udated by'] = None
        dict['pub date'] = myGreeting.date.strftime("%Y-%m-%d %H:%M +0000")
        dict['date modified'] = None
        assert dict == myGreeting.greeting_to_dict()

#=======TEST FOR GUESTBOOK CLASS========
class TestGuestbook(TestBaseClass):

    #test function Guestbook.get_key(self):
    def test_guestbook_get_key(self):

        assert self.myGuestbook.get_key() == ndb.Key("Guestbook", self.guestbook_name)

    #test function Guestbook.get_latest(self, count):
    def test_guestbook_get_latest(self):

        count = 10
        listGreeting = Greeting.query(
                    ancestor= self.myGuestbook.get_key()).order(-Greeting.date).fetch(count)
        assert listGreeting == self.myGuestbook.get_latest(count)

    #test function Guestbook.delete_greeting(self, id):
    def test_guestbook_delete_greeting(self):

        #delete id = 1
        id = 1
        self.myGuestbook.delete_greeting(id)
        assert None == self.myGuestbook.get_greeting_by_id(id)

    #test function Guestbook.get_greeting_by_id(self, id):
    def test_guestbook_get_greeting_by_id(self):
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
    def test_function_guestbook_put_greeting(self):

        author = "Author added"
        content = "Content added"
        #count number of greetings before put
        cursor = None
        more = True
        total = self.count_db(cursor, more)
        logging.warning(total)
        #number of greetings after put
        self.myGuestbook.put_greeting(author, content)
        cursor = None
        more = True
        total_new = self.count_db(cursor, more)
        assert total == total_new -1

    #function count db
    def count_db(self, cursor=None, more=True):
        self.LIMIT = 1024
        cursor = None
        more = True
        total = 0
        while more:
            ndbs, cursor, more = Greeting.get_page(self.guestbook_name,self.LIMIT,cursor)
            total += len(ndbs)
        return total

    #test function Guestbook.update_greeting(self, id, content, user):
    def test_fucntion_guestbook_update_greeting(self):

        #update greeting where id = 3
        id = 3
        content = "Content updated"
        user = "Author updated"
        self.myGuestbook.update_greeting(id, content, user)
        #check whether greeting with id = 3, content = "Content updated", greeting.updated=user
        greeting = self.myGuestbook.get_greeting_by_id(id)
        assert greeting.content == content and greeting.updated_by == user

    #test function Guestbook.get_latest_memcache(self, count) without cache:
    def test_get_latest_no_cache(self):
        from mock import patch
        with patch('google.appengine.api.memcache.get') as func:
            func.return_value = None
            greetings = self.myGuestbook.get_latest_memcache(5)
            assert len(greetings) == 5
            func.assert_called_with("%s:greetings" %self.guestbook_name)

    #test function Guestbook.get_latest_memcache(self, count) with cache:
    def test_get_latest_with_cache(self):
        from mock import patch
        with patch('google.appengine.api.memcache.get') as func:
            val_return = self.myGuestbook.get_latest(5)
            func.return_value = val_return
            greetings = self.myGuestbook.get_latest_memcache(5)
            assert greetings == self.myGuestbook.get_latest(5)
            func.assert_called_with("%s:greetings" %self.guestbook_name)
