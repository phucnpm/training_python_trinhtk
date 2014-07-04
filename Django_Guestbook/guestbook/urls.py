from django.conf.urls import *
from guestbook.views import SignView, IndexView, Send

urlpatterns = patterns('',
    url(r'^sign/$', SignView.as_view(), name='sign'),
    url(r'^$', IndexView.as_view(), name ='index'),
    url(r'^send/$', Send.as_view(), name ='send'),
)