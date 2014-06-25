
import logging
import os
import urllib
from google.appengine.api import users
from google.appengine.ext import ndb
from google.appengine.api import memcache
import webapp2
import jinja2

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)



#default guestbook's name
DEFAULT_GUESTBOOK_NAME = 'default_guestbook'
#Get guestbook key by guestbook's name
def guestbook_key(guestbook_name=DEFAULT_GUESTBOOK_NAME):
    return ndb.Key('Guestbook', guestbook_name)
#Greeting class
class Greeting(ndb.Model):
    author = ndb.UserProperty()
    content = ndb.StringProperty()
    date = ndb.DateTimeProperty(auto_now_add=True)


#MainPage
class MainPage(webapp2.RequestHandler):
    def get(self):
        #guestbook_name get from field 'guestbook_name' or default = DEFAULT_GUESTBOOK_NAME
        guestbook_name = self.request.get('guestbook_name',
                                          DEFAULT_GUESTBOOK_NAME)
        #Query get data of greetings whose ancestor is key of current guestbook, sort desc by date
        greetings_query = Greeting.query(
                ancestor=guestbook_key(guestbook_name)).order(-Greeting.date)
        #Get data from memcache of current guestbook then assign this result for greetings
        greetings = memcache.get('%s:greetings' %guestbook_name)
        #If memcache does not exist:
        if greetings is None:
            #Get data from database
            greetings = greetings_query.fetch(10)
            #Then cache these data, if app can't cache, give an error message
            if not memcache.add('%s:greetings' %guestbook_name, greetings, 10000):
                logging.error('Memcache set failed')
        #Check whether user loged in
        if users.get_current_user():
            #Create link logout & text
            url = users.create_logout_url(self.request.uri)
            url_linktext = 'Logout'
        #Else
        else:
            #Create link login & text
            url = users.create_login_url(self.request.uri)
            url_linktext = 'Login'
        #context variables:
        template_values = {
            'greetings': greetings,
            'guestbook_name': urllib.quote_plus(guestbook_name),
            'url': url,
            'url_linktext': url_linktext,
        }
        #Use template
        template = JINJA_ENVIRONMENT.get_template('templates/index.html')
        #transfer these context variables into template
        self.response.write(template.render(template_values))
#Guestbook
class Guestbook(webapp2.RequestHandler):
    def post(self):
        #When user signs into guestbook, these following code will help to update greeting's information
        guestbook_name = self.request.get('guestbook_name',
                                          DEFAULT_GUESTBOOK_NAME)

        greeting = Greeting(parent=guestbook_key(guestbook_name))

        if users.get_current_user():
            greeting.author = users.get_current_user()

        greeting.content = self.request.get('content')
        #After put this greeting, clear cache
        if greeting.put():
            memcache.delete("%s:greetings" %guestbook_name)

        query_params = {'guestbook_name': guestbook_name}

        self.redirect('/?' + urllib.urlencode(query_params))


app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/sign', Guestbook)
], debug=True)
