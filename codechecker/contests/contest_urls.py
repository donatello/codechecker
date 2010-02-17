from django.conf.urls.defaults import *

urlpatterns = patterns('codechecker.contests.views',
        (r'^$', 'contests_default'),
        (r'^all/', 'show_all_contests'),
        (r'^(?P<contest_id>\d+)/$', 'show_contest'),
        (r'^(?P<contest_id>\d+)/(?P<action>\w+)/$', 'show_contest'),
        )
