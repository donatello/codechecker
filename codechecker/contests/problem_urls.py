from django.conf.urls.defaults import *

urlpatterns = patterns('codechecker.contests.views',
        (r'^$', 'problems_default'),
        (r'^all/', 'show_all_problems'),
        (r'^(?P<problem_id>\d+)/', 'show_problem'),
        (r'^(?P<problem_id>\d+)/(?P<action>\w+)/$', 'show_problem'),
        )
