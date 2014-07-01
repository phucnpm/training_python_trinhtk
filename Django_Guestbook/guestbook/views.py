# Create your views here.
import logging
import urllib
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView
from google.appengine.api import users
from google.appengine.api import memcache
from django.contrib.databrowse.plugins.calendars import IndexView
from guestbook.forms import SignForm
from guestbook.models import Guestbook


class IndexView(TemplateView):

        template_name = "guestbook/mainpage.html"
        #Methode get data from database
        DEFAULT_PAGE_SIZE = 10
        def get_context_data(self, **kwargs):
            guestbook_name = self.request.GET.get('guestbook_name', 'default_guestbook')
            myGuestbook = Guestbook(name= guestbook_name)
            greetings = memcache.get("%s:greetings" %myGuestbook.name)
            if greetings is None:
                #Get data from database
                greetings = myGuestbook.get_latest(self.DEFAULT_PAGE_SIZE)
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

class SignView(FormView):

        template_name = "guestbook/mainpage.html"
        form_class = SignForm
        def form_valid(self, form):
            guestbook_name = form.cleaned_data.get('guestbook_name')
            content = form.cleaned_data.get('content')
            myGuestbook = Guestbook(name=guestbook_name)
            if users.get_current_user():
                myGuestbook.put_greeting(users.get_current_user().nickname(), content)
            else:
                myGuestbook.put_greeting(None, content)
            self.success_url = '/?'+urllib.urlencode({'guestbook_name':guestbook_name})
            return super(SignView, self).form_valid(form)
        def form_invalid(self, form):
            self.template_name="guestbook/error.html"
            return super(SignView, self).form_invalid(form)
