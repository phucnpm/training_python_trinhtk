# Create your views here.
import logging

from django.http import HttpResponseRedirect
from django.views.generic.base import TemplateResponseMixin, ContextMixin, View
from google.appengine.api import users
from guestbook.models import Greeting
from google.appengine.api import  memcache
import urllib




class IndexView(TemplateResponseMixin, ContextMixin, View):
        template_name = "guestbook/mainpage.html"
        def get(self, request, *args, **kwargs):
             #guestbook_name get from field 'guestbook_name' or default = default_guestbook
            guestbook_name = request.GET.get('guestbook_name', 'default_guestbook')

            #Get data from memcache of current guestbook then assign this result for greetings

            greetings = memcache.get("%s:greetings" %guestbook_name)
            #If memcache does not exist:
            if greetings is None:
                #Get data from database
                greetings = self.get_queryset(guestbook_name).fetch(10)
                #Then cache these data, if app can't cache, give an error message
                if not memcache.add("%s:greetings" %guestbook_name, greetings, 10000):
                    logging.error("Memcache set failed")
            #Check whether user loged in
            if users.get_current_user():
                #Create link logout & text
                url = users.create_logout_url(request.get_full_path())
                url_linktext = 'Logout'
            #Else
            else:
                #Create link login & text
                url = users.create_login_url(request.get_full_path())
                url_linktext = 'Login'
            #context variables:
            kwargs['greetings'] = greetings
            kwargs['guestbook_name'] = guestbook_name
            kwargs['url'] = url
            kwargs['url_linktext']=url_linktext
            context = self.get_context_data(**kwargs)
            return self.render_to_response(context)
        #Methode get data from database
        def get_queryset(self, guestbook_name):
            return Greeting.query(
                    ancestor=Greeting.get_key_from_name(guestbook_name)).order(-Greeting.date)

             #render template
class SignView(TemplateResponseMixin, ContextMixin, View):
        template_name = "guestbook/mainpage.html"
        def post(self, request):
            if request.method == 'POST':
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
            return HttpResponseRedirect('/')