# Create your views here.
import logging
from django.contrib.databrowse.plugins.calendars import IndexView
from django.http import HttpResponseRedirect
from django.views.generic.base import TemplateView
from google.appengine.api import users
from guestbook.models import Greeting
from google.appengine.api import memcache
import urllib


class IndexView(TemplateView):

        template_name = "guestbook/mainpage.html"
        #Methode get data from database
        def get_queryset(self, guestbook_name):
            return Greeting.query(
                    ancestor=Greeting.get_key_from_name(guestbook_name)).order(-Greeting.date)
        def get_context_data(self, **kwargs):
            guestbook_name = self.request.GET.get('guestbook_name', 'default_guestbook')
            greetings = memcache.get("%s:greetings" %guestbook_name)
            if greetings is None:
                #Get data from database
                greetings = self.get_queryset(guestbook_name).fetch(10)
                #Then cache these data, if app can't cache, give an error message
                if not memcache.add("%s:greetings" %guestbook_name, greetings, 10000):
                    logging.error("Memcache set failed")
            context = super(IndexView,self).get_context_data(**kwargs)
            #Check whether user loged in
            if users.get_current_user():
                #Create link logout & text
                url = users.create_login_url(self.request.get_full_path())
                url_linktext = 'Logout'
            else:
                #Create link login & text
                url = users.create_logout_url(self.request.get_full_path())
                url_linktext = 'Login'
            context['greetings'] = greetings
            context['guestbook_name'] = guestbook_name
            context['url'] = url
            context['url_linktext']= url_linktext
            return context

class SignView(TemplateView):

        template_name = "guestbook/mainpage.html"
        def post(self, request, *args, **kwargs):
            #When user signs into guestbook, these following code will help to update greeting's information
            guestbook_name = request.POST.get('guestbook_name')
            guestbook_key = Greeting.get_key_from_name(guestbook_name)
            greeting = Greeting(parent=guestbook_key)
            if users.get_current_user():
                greeting.author = users.get_current_user().nickname()
            greeting.content = request.POST.get('content')
            #After put this greeting, clear cache
            if greeting.put():
                memcache.delete("%s:greetings" %guestbook_name)
            return HttpResponseRedirect('/?'+urllib.urlencode({'guestbook_name':guestbook_name}))