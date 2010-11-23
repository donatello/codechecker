from django.conf.urls.defaults import patterns

urlpatterns = patterns( ( r'^$', 'default' ),
        ( r'^all/', 'show_all_problems' ),
        ( r'^all/(?P<page>\d+)/$', 'show_all_problems' ),
        ( r'^(?P<problem_id>\d+)/$', 'show_problem' ),
        ( r'^(?P<problem_id>\d+)/submit/$', 'submit' ),
        ( r'^(?P<problem_id>\d+)/(?P<action>\w+)/$', 'show_problem' ),
        ( r'^(?P<problem_id>\d+)/(?P<action>\w+)/(?P<page>\d+)/$', 'show_problem' ),
        )

def default( request ):
    pass

def show_all_problems( request, page = 1 ):
    pass

def show_problem( request, problem_id, action = 'view', page = 1 ):
    pass

def submit( request, problem_id ):
    pass
