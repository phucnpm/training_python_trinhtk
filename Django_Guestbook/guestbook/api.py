from django.utils import simplejson as json
import logging
from django.http import HttpResponse, Http404
from google.appengine.datastore.datastore_query import Cursor
from django.views.generic.edit import FormView
from google.appengine.api import datastore_errors
from google.appengine.api import users
from google.appengine.ext import ndb
try:
    from google.appengine.api.labs import taskqueue
except ImportError:
    from google.appengine.api import taskqueue
from guestbook.forms import apiForm
from guestbook.models import Guestbook, Greeting


class JSONResponseMixin(object):
    def render_to_response(self, context):
        return self.get_json_response(self.convert_context_to_json(context))

    def get_json_response(self, content, **httpresponse_kwargs):
        return HttpResponse(content,
                                 content_type='application/json',
                                 **httpresponse_kwargs)

    def convert_context_to_json(self, context):
        return json.dumps(context)
class search(JSONResponseMixin, FormView):
    def get(self, request, *args, **kwargs):
        guestbook_name = kwargs['guestbook_name']
        try:
            curs = Cursor(urlsafe=self.request.GET.get('cursor'))
        except datastore_errors.BadValueError:
            raise Http404
        items, nextcurs, more = Greeting.query(
                    ancestor= ndb.Key(Guestbook, guestbook_name)).order(-Greeting.date).fetch_page(20, start_cursor=curs)
        i = 0
        dict_item={}
        for x in items:
            if x.last_update:
                dict_item[i] = {'author':x.author, 'content':x.content, 'last updated by':x.updated_by, 'pub date':x.date.strftime("%Y-%m-%d %H:%M +0000"), 'date modify':x.last_update.strftime("%Y-%m-%d %H:%M +0000")}
            else:
                dict_item[i] = {'author':x.author, 'content':x.content, 'last updated by':x.updated_by, 'pub date':x.date.strftime("%Y-%m-%d %H:%M +0000"), 'date modify':None}
            i +=1
        if i != 0:
            context =  {'count':i, 'cursor':nextcurs.urlsafe(), 'guestbook_name':guestbook_name, 'greetings':dict_item, 'more':more}
        else :
            context = {'count':i,'guestbook_name':guestbook_name, 'more':more, 'greetings':[]}
        return self.render_to_response(context)
    form_class = apiForm
#POST /api/guestbook/<guestbook_name>/greeting
    #
    # Create new greeting
    # Successful return Http 204
    # Fail return Http 404
    # Form invalid return Http 400
    # def post(self, request, *args, **kwargs):
    #     form_class = self.get_form_class()
    #     form = self.get_form(form_class)
    #     if form.is_valid():
    #         return self.form_valid(form)
    #     else:
    #         return self.form_invalid(form)
    def form_invalid(self, form):
        super(search, self).form_invalid(form)
        return HttpResponse(status=400)
    def form_valid(self, form):
        guestbook_name = self.request.POST.get('guestbook_name')
        myGuestbook = Guestbook(name=guestbook_name)
        content = self.request.POST.get('content')
        if users.get_current_user():
            author = users.get_current_user().nickname()
        else:
            author=None
        if Greeting(parent=myGuestbook.get_key(), author= author, content= content):
            return HttpResponse(status=204)
        else:
            return HttpResponse(status=404)
    def get_context_data(self, **kwargs):
        context = super(search,self).get_context_data(**kwargs)
        context['guestbook_name'] = self.request.POST.get('guestbook_name')
        logging.warning('%s' %context['guestbook_name'])
        return context
class searchID(JSONResponseMixin, FormView):
    template_name = "guestbook/api_form.html"
    form_class = apiForm
    def get(self, request, *args, **kwargs):
        guestbook_name = kwargs['guestbook_name']
        id = kwargs['id']
        myGuestBook = Guestbook(name=guestbook_name)
        x = myGuestBook.get_greeting_by_id(id)
        if x:
            if x.last_update:
                dict_item = {'author':x.author, 'content':x.content, 'last updated by':x.updated_by, 'pub date':x.date.strftime("%Y-%m-%d %H:%M +0000"), 'date modify':x.last_update.strftime("%Y-%m-%d %H:%M +0000")}
            else:
                dict_item = {'author':x.author, 'content':x.content, 'last updated by':x.updated_by, 'pub date':x.date.strftime("%Y-%m-%d %H:%M +0000"), 'date modify':None}
            context = {'guestbook_name':guestbook_name, 'greetings':dict_item}
            return self.render_to_response(context)
        else:
            raise Http404
    def form_valid(self, form):
        guestbook_name = self.request.POST.get('guestbook_name')
        id = self.request.POST.get('id')
        content = self.request.POST.get('content')
        myGuestbook = Guestbook(name=guestbook_name)
        if users.get_current_user():
            author = users.get_current_user().nickname()
            myGuestbook.update_greeting(id, content, author)
            return HttpResponse(status=204)
        else:
            return HttpResponse(status=404)
    def form_invalid(self, form):
        return HttpResponse(status=400)
    def delete(self, request, *args, **kwargs):
        guestbook_name = self.request.POST.get('guestbook_name')
        id = self.request.POST.get('id')
        myGuestbook = Guestbook(name=guestbook_name)
        if users.is_current_user_admin():
            myGuestbook.delete_greeting(id)
            return HttpResponse(status=204)
        else:
            return HttpResponse(status=404)