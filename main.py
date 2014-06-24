import cgi
import cStringIO
import logging
import urllib
import webapp2

from google.appengine.ext import db
from google.appengine.api import memcache
from google.appengine.api import users

default_guestbook = 'Welcome'
class Greeting(db.Model):
    author = db.StringProperty()
    content = db.StringProperty(multiline=True)
    date = db.DateTimeProperty(auto_now_add=True)


def guestbook_key(guestbook_name=None):
    return db.Key.from_path('Guestbook', guestbook_name or 'default_guestbook')


class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.out.write('<html><body>')
        guestbook_name = self.request.get('guestbook_name')
        if guestbook_name == '':
            guestbook_name = default_guestbook
        greetings = self.get_greetings(guestbook_name)
        stats = memcache.get_stats()

        self.response.out.write(greetings)
        if users.get_current_user():
            url = users.create_logout_url(self.request.uri)
            url_linktext = 'Logout'
        else:
            url = users.create_login_url(self.request.uri)
            url_linktext = 'Login'
        self.response.out.write("""
          <form action="/sign?%s" method="post">
            <div><textarea name="content" rows="3" cols="60"></textarea></div>
            <div><input type="submit" value="Sign Guestbook"></div>
          </form>
          <hr>
          <form>Guestbook name: <input value="%s" name="guestbook_name">
          <input type="submit" value="switch"></form>
          <a href="%s">%s</a>
        </body>
      </html>""" % (urllib.urlencode({'guestbook_name': guestbook_name}),
                          cgi.escape(guestbook_name), url, url_linktext))

    def get_greetings(self, guestbook_name):

        greetings = memcache.get('%s:greetings' % guestbook_name)
        if greetings is not None:
            return greetings
        else:
            greetings = self.render_greetings(guestbook_name)
            if not memcache.add('%s:greetings' % guestbook_name, greetings, 10):
                logging.error('Memcache set failed.')
        return greetings

    def render_greetings(self, guestbook_name):

        greetings = db.GqlQuery('SELECT * '
                                'FROM Greeting '
                                'WHERE ANCESTOR IS :1 '
                                'ORDER BY date DESC LIMIT 10',
                                guestbook_key(guestbook_name))
        output = cStringIO.StringIO()
        for greeting in greetings:
            if greeting.author:
                output.write('<b>%s</b> wrote:' % greeting.author)
            else:
                output.write('An anonymous person wrote:')
            output.write('<blockquote>%s</blockquote>' %
                         cgi.escape(greeting.content))
        return output.getvalue()


class Guestbook(webapp2.RequestHandler):
    def post(self):
        guestbook_name = self.request.get('guestbook_name')
        greeting = Greeting(parent=guestbook_key(guestbook_name))

        if users.get_current_user():
            greeting.author = users.get_current_user().nickname()
        greeting.content = self.request.get('content')
        greeting.put()
        self.redirect('/?' + urllib.urlencode({'guestbook_name': guestbook_name}))


app = webapp2.WSGIApplication([('/', MainPage),
                               ('/sign', Guestbook)],
                              debug=True)