# Create your views here.
import logging
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.views.generic.base import TemplateResponseMixin, ContextMixin, View
from google.appengine.api import users
from guestbook.models import Greeting
from google.appengine.api import  memcache
import urllib

# def main_page(request):
#      #guestbook_name get from field 'guestbook_name' or default = default_guestbook
#     guestbook_name = request.GET.get('guestbook_name', 'default_guestbook')
#
#     guestbook_key = Greeting.get_key_from_name(guestbook_name)
#
#     #Get data from memcache of current guestbook then assign this result for greetings
#
#     greetings = memcache.get("%s:greetings" %guestbook_name)
#     #If memcache does not exist:
#     if greetings is None:
#         #Get data from database
#         #Query get data of greetings whose ancestor is key of current guestbook, sort desc by date
#         greetings_query = Greeting.query(
#             ancestor=Greeting.get_key_from_name(guestbook_name)).order(-Greeting.date)
#         greetings = greetings_query.fetch(10)
#         #Then cache these data, if app can't cache, give an error message
#         if not memcache.add("%s:greetings" %guestbook_name, greetings, 10000):
#             logging.error("Memcache set failed")
#     #Check whether user loged in
#     if users.get_current_user():
#         #Create link logout & text
#         url = users.create_logout_url(request.get_full_path())
#         url_linktext = 'Logout'
#     #Else
#     else:
#         #Create link login & text
#         url = users.create_login_url(request.get_full_path())
#         url_linktext = 'Login'
#     #context variables:
#     template_values = {
#         'greetings': greetings,
#         'guestbook_name': guestbook_name,
#         'url': url,
#         'url_linktext' : url_linktext,
#
#     }
#      #render template
#     return render(request, 'guestbook/mainpage.html', template_values)
# def sign_post(request):
#     if request.method == 'POST':
#     #When user signs into guestbook, these following code will help to update greeting's information
#         guestbook_name = request.POST.get('guestbook_name')
#         guestbook_key = Greeting.get_key_from_name(guestbook_name)
#         greeting = Greeting(parent=guestbook_key)
#         if users.get_current_user():
#             greeting.author = users.get_current_user().nickname()
#         greeting.content = request.POST.get('content')
#     #After put this greeting, clear cache
#         if greeting.put():
#             memcache.delete("%s:greetings" %guestbook_name)
#         return HttpResponseRedirect('/?'+urllib.urlencode({'guestbook_name':guestbook_name}))
#     return HttpResponseRedirect('/')

class TemplateView(TemplateResponseMixin, ContextMixin, View):
    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)
    def post(self, request):
        return HttpResponseRedirect('/')
class IndexView(TemplateView):
        template_name = "guestbook/mainpage.html"
        def get(self, request, *args, **kwargs):
             #guestbook_name get from field 'guestbook_name' or default = default_guestbook
            guestbook_name = request.GET.get('guestbook_name', 'default_guestbook')

            guestbook_key = Greeting.get_key_from_name(guestbook_name)

            #Get data from memcache of current guestbook then assign this result for greetings

            greetings = memcache.get("%s:greetings" %guestbook_name)
            #If memcache does not exist:
            if greetings is None:
                #Get data from database
                #Query get data of greetings whose ancestor is key of current guestbook, sort desc by date
                greetings_query = Greeting.query(
                    ancestor=Greeting.get_key_from_name(guestbook_name)).order(-Greeting.date)
                greetings = greetings_query.fetch(10)
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
            return super(IndexView, self).get(request, *args, **kwargs)
             #render template
class SignView(TemplateView):
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
            return super(SignView, self).post(request)