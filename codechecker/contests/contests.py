from django.conf.urls.defaults import patterns

urlpatterns = patterns( 'codechecker.contests.contests',
        ( r'^$', 'default' ),
        ( r'^all/$', 'show_all_contests' ),
        ( r'^all/(?P<page>\d+)/$', 'show_all_contests' ),
        ( r'^(?P<contest_id>\d+)/$', 'show_contest' ),
        ( r'^(?P<contest_id>\d+)/(?P<action>\w+)/$', 'show_contest' ),
        ( r'^(?P<contest_id>\d+)/(?P<action>\w+)/(?P<page>\d+)/$', 'show_contest' ),
        )

def default( request ):
    pass

def show_all_contests( request, page = 1 ):
    pass

def show_contest( request, contest_id = None, action = 'view', page = 1 ):
    pass
