from django.utils import simplejson as json
import logging
from django.http import HttpResponse
from google.appengine.datastore.datastore_query import Cursor
from django.views.generic.edit import FormView
from google.appengine.api import datastore_errors
from google.appengine.api import users
try:
    from google.appengine.api.labs import taskqueue
except ImportError:
    from google.appengine.api import taskqueue
from guestbook.forms import ApiForm
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


class Search(JSONResponseMixin, FormView):
#       GET /api/guestbook/<guestbook_name>/greeting
#
#  return JSON: guestbookname as STRING, more as BOOL, next_cursor as STRING, 20 lastest greetings
#       GET /api/guestbook/<guestbook_name>/greeting?cursor=<urlsafe_next_cursor>
#         return 20 next greetings
#       return Http 404 if query error

    def get(self, request, *args, **kwargs):
        guestbook_name = kwargs['guestbook_name']
        try:
            curs = Cursor(urlsafe=self.request.GET.get('cursor'))
        except datastore_errors.BadValueError:
            return HttpResponse(status=404)
        items, nextcurs, more = Greeting.get_page(guestbook_name, 20, curs)
        dict_item = [x.greeting_to_dict() for x in items]
        context = {}
        context["guestbook_name"] = guestbook_name
        context["greetings"] = dict_item
        context["more"] = more
        if more:
            context["cursor"] = nextcurs.urlsafe()
        context["count"] = len(items)
        return self.render_to_response(context)
# POST /api/guestbook/<guestbook_name>/greeting
#
#     Create new greeting
#     Successful return Http 204
#     Fail return Http 404
#     Form invalid return Http 400

    form_class = ApiForm

    def form_invalid(self, form):
        return HttpResponse(status=400)

    def form_valid(self, form):
        guestbook_name = self.kwargs('guestbook_name')
        myguestbook = Guestbook(name=guestbook_name)
        content = self.request.POST.get('content')
        if users.get_current_user():
            author = users.get_current_user().nickname()
        else:
            author = None
        if Greeting(parent=myguestbook.get_key(), author=author, content=content):
            return HttpResponse(status=204)
        else:
            return HttpResponse(status=404)

    def get_context_data(self, **kwargs):
        context = super(Search, self).get_context_data(**kwargs)
        context['guestbook_name'] = self.kwargs('guestbook_name')
        logging.warning('%s' % context['guestbook_name'])
        return context


class SearchID(JSONResponseMixin, FormView):

    form_class = ApiForm

# GET /api/guestbook/<guestbook_name>/greeting/<id>
#
#     return JSON: greeting id, content, date, updated_by, updated_date, guestbook_name
#     return Http 404 if cannot retrieve

    def get(self, request, *args, **kwargs):
        guestbook_name = kwargs['guestbook_name']
        id = kwargs['id']
        myguestbook = Guestbook(name=guestbook_name)
        x = myguestbook.get_greeting_by_id(id)
        if x:
            dict_item = x.greeting_to_dict()
            context = {}
            context['guestbook_name'] = guestbook_name
            context['greetings'] = dict_item
            return self.render_to_response(context)
        else:
            return HttpResponse(status=404)

# PUT /api/guestbook/<guestbook_name>/greeting/<id>
#
#     update date greeting via parameters same as POST
#     Successful return Http 204
#     Fail return Http 404
#     Form invalid return Http 400
#

    def form_valid(self, form):
        guestbook_name = self.kwargs('guestbook_name')
        id = self.kwargs('id')
        content = self.request.POST.get('content')
        myguestbook = Guestbook(name=guestbook_name)
        greeting = myguestbook.get_greeting_by_id(id)
        if users.is_current_user_admin() or users.get_current_user().nickname() == greeting.author:
            author = users.get_current_user().nickname()
            myguestbook.update_greeting(id, content, author)
            return HttpResponse(status=204)
        else:
            return HttpResponse(status=404)

    def form_invalid(self, form):

        return HttpResponse(status=400)

# DELETE /api/guestbook/<guestbook_name>/greeting/<id>
#
#     delete greeting
#     Successful return Http 204
#     Fail return Http 404

    def delete(self, request, *args, **kwargs):
        guestbook_name = kwargs['guestbook_name']
        id = kwargs['id']
        myguestbook = Guestbook(name=guestbook_name)
        if users.is_current_user_admin():
            myguestbook.delete_greeting(id)
            return HttpResponse(status=204)
        else:
            return HttpResponse(status=404)