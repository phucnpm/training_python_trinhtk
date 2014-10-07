from django.utils import simplejson as json
import logging
from django.http import HttpResponse, QueryDict
from google.appengine.datastore.datastore_query import Cursor
from django.views.generic.edit import FormView
from google.appengine.api import datastore_errors
from google.appengine.api import users
from google.appengine.ext import ndb
try:
	from google.appengine.api.labs import taskqueue
except ImportError:
	from google.appengine.api import taskqueue
from guestbook.forms import ApiForm
from guestbook.models import Guestbook, Greeting
import json


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
	#  return JSON: guestbookname as STRING, more as BOOL, next_cursor as STRING,
	#  20 lastest greetings
	#       GET /api/guestbook/<guestbook_name>/greeting?cursor=<urlsafe_next_cursor>
	#         return 20 next greetings
	#       return Http 404 if query error

	def get(self, request, *args, **kwargs):
		guestbook_name = kwargs['guestbook_name']
		try:
			curs = Cursor(urlsafe=self.request.GET.get('cursor'))
			lim = int(self.request.GET.get('limit'))
			key_search = self.request.GET.get('keySearch')
		except datastore_errors.BadValueError:
			return HttpResponse(status=404)
		items, nextcurs, more = Greeting.get_page(guestbook_name, lim, curs, key_search)
		if not key_search:
			count = Greeting.query(ancestor=ndb.Key(Guestbook, guestbook_name)).count()
		else:
			count = Greeting.query(ancestor=ndb.Key(Guestbook, guestbook_name)).\
				filter(Greeting.content == key_search).count()
		dict_item = [x.greeting_to_dict() for x in items]
		context = {}
		context["is_admin"] = users.is_current_user_admin()
		context["guestbook_name"] = guestbook_name
		context["greetings"] = dict_item
		context["more"] = more
		if more:
			context["cursor"] = nextcurs.urlsafe()
		context['itemLoaded'] = len(items)
		context["totalItems"] = count
		return self.render_to_response(context)
	# POST /api/guestbook/<guestbook_name>/greeting
	#
	#     Create new greeting
	#     Successful return Http 204
	#     Fail return Http 404
	#     Form invalid return Http 400

	form_class = ApiForm

	def post(self, request, *args, **kwargs):
		#<bound method QueryDict.get of <QueryDict: {}>
		#If request.POST is null -> request.Post = request.body to dict
		request.POST = json.loads(request.body)
		content = request.POST.get('content')
		return super(Search, self).post(request, args, kwargs)

	def form_invalid(self, form):
		return HttpResponse(status=400)

	def form_valid(self, form):
		guestbook_name = self.kwargs['guestbook_name']
		myguestbook = Guestbook(name=guestbook_name)
		content = self.request.POST.get('content')
		if users.get_current_user():
			author = users.get_current_user().nickname()
		else:
			author = None
		id = myguestbook.put_greeting(author, content)
		if id is not False:
			res = {}
			res['id_greeting'] = id
			return self.render_to_response(res)
		else:
			return HttpResponse(status=404)

	def get_context_data(self, **kwargs):
		context = super(Search, self).get_context_data(**kwargs)
		context['guestbook_name'] = self.kwargs('guestbook_name')
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
	# PUT is a valid HTTP verb for creating (with a known URL) or editing an
	# object, note that browsers only support POST for now.

	def put(self, request, *args, **kwargs):
		#If request.POST is null -> request.Post = request.body to dict
		request.POST = json.loads(request.body)
		return self.post(request, *args, **kwargs)

	def form_valid(self, form):
		self.request.POST = json.loads(self.request.body)
		guestbook_name = self.kwargs['guestbook_name']
		id = self.kwargs['id']
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