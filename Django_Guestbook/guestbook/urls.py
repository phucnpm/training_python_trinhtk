from django.conf.urls import *
from guestbook.views import SignView, IndexView, Send, Delete, Edit, EditSuccess

urlpatterns = patterns('',
    url(r'^sign/$', SignView.as_view(), name='sign'),
    url(r'^$', IndexView.as_view(), name ='index'),
    url(r'^send/$', Send.as_view(), name ='send'),
    url(r'^delete/$', Delete.as_view(), name ='delete'),
    url(r'^edit/$', Edit.as_view(), name ='edit'),
    url(r'^editsuccess/$', EditSuccess.as_view(), name ='edit'),
)