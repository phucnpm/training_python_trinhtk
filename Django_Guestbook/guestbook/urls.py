from django.conf.urls.defaults import *
from guestbook.views import SignView, IndexView

urlpatterns = patterns('',
    url(r'^sign/$', SignView.as_view(), name='sign'),
    url(r'^$', IndexView.as_view(), name ='index'),
)