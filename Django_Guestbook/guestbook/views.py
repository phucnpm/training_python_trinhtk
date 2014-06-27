# Create your views here.
import logging
from django.contrib.databrowse.plugins.calendars import IndexView
from django.http import HttpResponseRedirect
from django.views.generic.base import TemplateView
from google.appengine.api import users
from guestbook.models import Greeting, Guestbook
from google.appengine.api import memcache
import urllib


class IndexView(TemplateView):


        template_name = "guestbook/mainpage.html"
        #Methode get data from database

        def get_queryset(self, guestbook_key):

            return Greeting.query(
                    ancestor=guestbook_key).order(-Greeting.date)

        def get_context_data(self, **kwargs):

            guestbook_name = self.request.GET.get('guestbook_name', 'default_guestbook')
            myGuestbook = Guestbook(name= guestbook_name)
            greetings = memcache.get("%s:greetings" %myGuestbook.name)
            if greetings is None:
                #Get data from database
                greetings = self.get_queryset(myGuestbook.get_key(myGuestbook.name)).fetch(10)
                #Then cache these data, if app can't cache, give an error message
                if not memcache.add("%s:greetings" %myGuestbook.name, greetings, 10000):
                    logging.error("Memcache set failed")
            context = super(IndexView,self).get_context_data(**kwargs)
            #Check whether user loged in
            if users.get_current_user():
                #Create link logout & text
                url = users.create_logout_url(self.request.get_full_path())
                url_linktext = 'Logout'
            else:
                #Create link login & text
                url = users.create_login_url(self.request.get_full_path())
                url_linktext = 'Login'
            context['greetings'] = greetings
            context['guestbook_name'] = myGuestbook.name
            context['url'] = url
            context['url_linktext']= url_linktext
            return context

class SignView(TemplateView):


        template_name = "guestbook/mainpage.html"
        
        def post(self, request, *args, **kwargs):

            #When user signs into guestbook, these following code will help to update greeting's information
            guestbook_name = request.POST.get('guestbook_name')
            myGuestbook = Guestbook(name=guestbook_name)
            if users.get_current_user():
                greeting = Greeting(parent=myGuestbook.get_key(myGuestbook.name), author= users.get_current_user().nickname(), content=request.POST.get('content'))
            else:
               greeting = Greeting(parent=myGuestbook.get_key(myGuestbook.name), author= None, content=request.POST.get('content'))
            #After put this greeting, clear cache
            if greeting.put():
                memcache.delete("%s:greetings" %guestbook_name)
            return HttpResponseRedirect('/?'+urllib.urlencode({'guestbook_name':guestbook_name}))