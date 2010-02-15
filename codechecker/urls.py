from django.conf.urls.defaults import *
from django.contrib.auth import views as auth_views
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^codechecker/', include('codechecker.foo.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),

    # default Generic Views
    (r'^$', 'codechecker.generic_views.default'),
    (r'^about/', 'codechecker.generic_views.default', { 'action' : 'about'}),
    (r'^reference/', 'codechecker.generic_views.default', { 'action' : 'references'}),
    
    # User Related Views
    (r'login/$', auth_views.login, { 'template_name' : 'accounts/login.html', }),
    (r'logout/$',auth_views.logout, { 'next_page' : '/site/', }), 

    #Contest Related Views
    (r'^contests/', include('codechecker.contests.contest_urls')),
    (r'^problems/', include('codechecker.contests.problem_urls')),
)
