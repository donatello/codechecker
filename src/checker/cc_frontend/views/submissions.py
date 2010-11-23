from django.conf.urls.defaults import *

urlpatterns = patterns( ( r'^$', 'default' ),
        ( r'^(?P<page>\d+)/$', 'handle' ),
        ( r'^contests/(?P<contest_id>\d+)/$', 'handle' ),
        ( r'^contests/(?P<contest_id>\d+)/(?P<page>\d+)/$', 'handle' ),
        ( r'^problems/(?P<problem_id>\d+)/$', 'handle' ),
        ( r'^problems/(?P<problem_id>\d+)/(?P<page>\d+)/$', 'handle' ),
        )
def default( request ):
    pass

def handle( request, page = 1, contest_id = None, problem_id = None ):
    pass
