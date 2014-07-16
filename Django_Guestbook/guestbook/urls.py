from django.conf.urls import *
from django.views.generic.base import TemplateView
from guestbook.views import SignView, IndexView

urlpatterns = patterns('',
    url(r'^sign/$', SignView.as_view(), name='sign'),
    url(r'^$', IndexView.as_view(), name ='index'),
    url(r'^ui$', TemplateView.as_view(template_name='guestbook/ui.html'), name ='ui')
)