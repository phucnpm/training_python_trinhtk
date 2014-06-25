from django.conf.urls.defaults import *
from guestbook.views import sign_post, IndexView

urlpatterns = patterns('',
    (r'^sign/$', sign_post),
    url(r'^$', IndexView.as_view(), name ='index'),
)