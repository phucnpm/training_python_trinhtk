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
        while i <= 19:
            key = Greeting(parent=self.myGuestbook.get_key(), author="Author test %s" % i,
                           content='Content test %s' % i).put()
            i += 1

    def teardown_method(self, method):
        self.testbed.deactivate()


#=======TEST FOR GREETING CLASS========
class Test_Greeting(TestBaseClass):

    #test function Greeting.get_page(cls, guestbook_name, pagesize, cursor=None):
    #load 10, len = 10
    def test_greeting_get_page_len_less_than_total(self):
        curs = None
        pagesize = 10
        ndbs, cursor, more = Greeting.get_page(self.guestbook_name, pagesize, curs)
        assert len(ndbs) == 10

    #load 30, max = 20
    def test_greeting_get_page_len_greater_than_total(self):
        curs = None
        pagesize = 30
        ndbs, cursor, more = Greeting.get_page(self.guestbook_name, pagesize, curs)
        assert len(ndbs) >= 20 and len(ndbs) < 30

    #load = 0
    def test_greeting_get_page_len_equal_zero(self):
        curs = None
        pagesize = 0
        ndbs, cursor, more = Greeting.get_page(self.guestbook_name, pagesize, curs)
        assert ndbs is None

    #load < 0
    def test_greeting_get_page_len_less_than_zero(self):
        curs = None
        pagesize = -1
        ndbs, cursor, more = Greeting.get_page(self.guestbook_name, pagesize, curs)
        assert ndbs is None

    # dust curs
    def test_greeting_get_page_dust_curs(self):
        curs = "asdosdhfoiqhio341"
        pagesize = 10
        ndbs, cursor, more = Greeting.get_page(self.guestbook_name, pagesize, curs)
        assert ndbs is None

    #test function Greeting.greeting_to_dict(self):
    def test_greeting_to_dict(self):
        greeting = Greeting.query(Greeting.content == "Content test 1",
                                  Greeting.author == "Author test 1").fetch(1)[0]
        id = greeting.key.id()
        mygreeting = self.myGuestbook.get_greeting_by_id(id)
        dict = {}
        dict["author"] = "Author test 1"
        dict['content'] = "Content test 1"
        dict['last udated by'] = None
        dict['pub date'] = mygreeting.date.strftime("%Y-%m-%d %H:%M +0000")
        dict['date modified'] = None
        assert dict == mygreeting.greeting_to_dict()


#=======TEST FOR GUESTBOOK CLASS========
class TestGuestbook(TestBaseClass):

    #test function Guestbook.get_latest(self, count):
    def test_guestbook_get_latest(self):
        author1 = "Author added 1"
        content1 = "Content added 1"
        author2 = "Author added 2"
        content2 = "Content added 2"
        self.myGuestbook.put_greeting(author1, content1)
        self.myGuestbook.put_greeting(author2, content2)
        count = 2
        listgreeting = Greeting.query(
            ancestor=self.myGuestbook.get_key()).order(-Greeting.date).fetch(count)
        #list[0] = (content2, author2) --- list[1] = (content1, author1)
        assert listgreeting[0].content == content2 and listgreeting[1].content == content1

    #test function Guestbook.delete_greeting(self, id):
    def test_guestbook_delete_greeting(self):
        #delete id = 1
        cursor = None
        more = True
        total = self.count_db(cursor, more)
        #total = 20
        mygreeting = self.myGuestbook.get_latest(1)
        id = mygreeting[0].key.id()
        self.myGuestbook.delete_greeting(id)
        cursor = None
        more = True
        total_new = self.count_db(cursor, more)
        #total_new = 19
        assert total == total_new + 1

    #test function Guestbook.get_greeting_by_id(self, id):
    def test_guestbook_get_greeting_by_id(self):
        mygreeting = self.myGuestbook.get_latest(1)[0]
        id = mygreeting.key.id()
        assert mygreeting == self.myGuestbook.get_greeting_by_id(id)

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
        #number of greetings after put
        self.myGuestbook.put_greeting(author, content)
        cursor = None
        more = True
        total_new = self.count_db(cursor, more)
        assert total == total_new - 1

    #function count db
    def count_db(self, cursor=None, more=True):
        self.LIMIT = 1024
        cursor = None
        more = True
        total = 0
        while more:
            ndbs, cursor, more = Greeting.get_page(self.guestbook_name, self.LIMIT, cursor)
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
            func.assert_called_with("%s:greetings" % self.guestbook_name)

    #test function Guestbook.get_latest_memcache(self, count) with cache:
    def test_get_latest_with_cache(self):
        from mock import patch
        with patch('google.appengine.api.memcache.get') as func:
            val_return = "VALUE RETURN"
            func.return_value = val_return
            greetings = self.myGuestbook.get_latest_memcache(1)
            assert greetings == "VALUE RETURN"
            func.assert_called_with("%s:greetings" % self.guestbook_name)
