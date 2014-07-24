from django.conf.urls import *
from django.views.generic import TemplateView
from guestbook.api import Search, SearchID
from guestbook.views import SignView, IndexView, Send, Delete, Edit, ClientView


urlpatterns = patterns('',
    url(r'^sign/$', SignView.as_view(), name='sign'),
    url(r'^$', IndexView.as_view(), name ='index'),
    url(r'^send/$', Send.as_view(), name ='send'),
    url(r'^delete/$', Delete.as_view(), name ='delete'),
    url(r'^edit/$', Edit.as_view(), name ='edit'),
    url(r'^api/guestbook/(?P<guestbook_name>[a-zA-Z0-9\s\+\_]+)/greeting/$',Search.as_view()),
    url(r'^api/guestbook/(?P<guestbook_name>[a-zA-Z0-9\s\+\_]+)/'
        r'greeting/(?P<id>[a-zA-Z0-9\s\+\_]+)/$',SearchID.as_view()),
    url(r'^client/$',ClientView.as_view(), name='ui')
)