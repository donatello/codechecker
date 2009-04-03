from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^checker/', include('checker.foo.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/(.*)', admin.site.root),
    # Default Page view
    (r'^$', 'checker.contests.views.default_view'),
    
    # Contests Listing Page
    (r'contests/$','checker.contests.contests_view.handle'),
    
    # Problems Listing Page
    (r'contests/([^/]*)','checker.contests.problems_view.handle'),
    
    (r'problems/$','checker.contests.problems_view.list_all_problems'),
    (r'problems/page/(\d+)/','checker.contests.problems_view.handle_pages'),
    (r'problems/([a-zA-Z0-9-_]+)/','checker.contests.problems_view.view_problem'),
    (r'login/$', 'django.contrib.auth.views.login'),
    (r'logout/$', 'checker.contests.logout.handle'),
    (r'submit/','checker.contests.submit.handle'),
    (r'status/$','checker.contests.status.handle'),
    (r'status/([0-9]+)/','checker.contests.status.handle2'),                      
    (r'ranklist/$','checker.contests.status.ranklists'),
    (r'faq/','checker.contests.status.faq'),
    (r'accounts/','checker.contests.logout.accounts'),
    (r'password_change/$','checker.contests.logout.password_change'),
    (r'register/','checker.contests.registration.register'),
)
