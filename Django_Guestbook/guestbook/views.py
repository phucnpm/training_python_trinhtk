# Create your views here.
from datetime import date
import logging
import urllib
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView
from google.appengine.api import users
from google.appengine.api import memcache
from google.appengine.api import mail
from django.contrib.databrowse.plugins.calendars import IndexView
from google.appengine.ext import ndb
try:
    from google.appengine.api.labs import taskqueue
except ImportError:
    from google.appengine.api import taskqueue
from guestbook.forms import SignForm, EditForm
from guestbook.models import Guestbook


class IndexView(TemplateView):

        template_name = "guestbook/mainpage.html"
        #Methode get data from database
        DEFAULT_PAGE_SIZE = 10

        def get_context_data(self, **kwargs):
            guestbook_name = self.request.GET.get('guestbook_name', 'default_guestbook')
            myGuestbook = Guestbook(name=guestbook_name)
            greetings = myGuestbook.get_latest_memcache(self.DEFAULT_PAGE_SIZE)
            context = super(IndexView, self).get_context_data(**kwargs)
            #Check whether user loged in
            if users.get_current_user():
                #Create link logout & text
                url = users.create_logout_url(self.request.get_full_path())
                url_linktext = 'Logout'
                context['current_user'] = users.get_current_user().nickname()
            else:
                #Create link login & text
                url = users.create_login_url(self.request.get_full_path())
                url_linktext = 'Login'

            context['is_admin'] = users.is_current_user_admin()
            context['greetings'] = greetings
            context['guestbook_name'] = myGuestbook.name
            context['url'] = url
            context['url_linktext'] = url_linktext
            return context


class SignView(FormView):
        template_name = "guestbook/mainpage.html"
        form_class = SignForm

        def form_valid(self, form):
            #When form is valid, guestbook name = get data of field named guestbook_name, content =
            #  get data of field named content
            guestbook_name = form.cleaned_data.get('guestbook_name')
            content = form.cleaned_data.get('content')
            #create new guestbook with its name = guestbook_name
            myGuestbook = Guestbook(name=guestbook_name)
            #if user loged in, taskqueue will add this task with params : guestbook_name, author,
            #  content
            if users.get_current_user():
                myGuestbook.put_greeting(users.get_current_user().nickname(), content)
            #else, author = none
            else:
                myGuestbook.put_greeting(None, content)
            #after add task, redirect to success_url
            self.success_url = '/?'+urllib.urlencode({'guestbook_name': guestbook_name})
            return super(SignView, self).form_valid(form)
            #When form is invalid, generate error page

        def form_invalid(self, form):
            self.template_name = "guestbook/error.html"
            return super(SignView, self).form_invalid(form)


class Send(TemplateView):
        #Send mail in get function with params: guestbook_name, author, content
        @ndb.transactional
        def get(self, request, *args, **kwargs):
            mail.send_mail(sender="Application <khtrinh.tran@gmail.com>",
                           to="Admin<kingsley13693@gmail.com>",
                           subject="New greeting has been signed",
                           body="""
               Guestbook: %s
               Author: %s
               Content: %s
                """ % (self.request.GET.get("guestbook_name"), self.request.GET.get("author"),
                       self.request.GET.get("content")))
            #after send mail, generate a message
            return HttpResponse('Email has been sent')


class Delete(TemplateView):
        @ndb.transactional
        def get(self, request, *args, **kwargs):
            guestbook_name = self.request.GET.get("guestbook_name")
            id = self.request.GET.get("id")
            myGuestbook = Guestbook(name=guestbook_name)
            if users.is_current_user_admin():
                myGuestbook.delete_greeting(id)
                return HttpResponseRedirect('/?'
                                            + urllib.urlencode({'guestbook_name': guestbook_name}))
            return HttpResponse("You are not administrator :)")


class Edit(FormView):
        template_name = "guestbook/edit.html"
        form_class = EditForm

        def get(self, request, *args, **kwargs):
            guestbook_name = self.request.GET.get("guestbook_name")
            id = self.request.GET.get("id")
            myGuestbook = Guestbook(name=guestbook_name)
            greeting = myGuestbook.get_greeting_by_id(id)
            return self.render_to_response(
                self.get_context_data(greeting=greeting,
                                      guestbook_name=guestbook_name, id=id))

        def form_valid(self, form):
            #When form is valid, guestbook name = get data of field named guestbook_name,
            #  content = get data of field named content
            guestbook_name = form.cleaned_data.get('guestbook_name')
            content = form.cleaned_data.get('content')
            id = form.cleaned_data.get('id')
            #create new guestbook with its name = guestbook_name
            myGuestbook = Guestbook(name=guestbook_name)
            au = users.get_current_user().nickname()
            myGuestbook.update_greeting(id, content, au)
            self.success_url = '/?'+urllib.urlencode({'guestbook_name': guestbook_name})
            return super(Edit, self).form_valid(form)
            #When form is invalid, generate error page

        def form_invalid(self, form):
            self.template_name = "guestbook/edit.html"
            return super(Edit, self).form_invalid(form)
