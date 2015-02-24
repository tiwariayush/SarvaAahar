from django.conf.urls import url, patterns, include
from middaymeal.views import *

urlpatterns = patterns('',
    url(r'^$', EditChild),
#    url(r'edit/(?P<child_id>\d+)/$', EditChild),
)
