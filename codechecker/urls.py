import django
from django.conf.urls.defaults import *
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns( '',
    # Example:
    # (r'^codechecker/', include('codechecker.foo.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    ( r'^admin/doc/', include( 'django.contrib.admindocs.urls' ) ),

    # Uncomment the next line to enable the admin:
    ( r'^admin/', include( admin.site.urls ) ),

    # default Generic Views
    ( r'^$', 'codechecker.views.default' ),
    ( r'about/$', 'codechecker.views.default', { 'action' : 'about'} ),
    ( r'references/$', 'codechecker.views.default', { 'action' : 'references'} ),

    # Contest App based views
    ( r'/contests/', include( 'codechecker.contests.contests' ) ),
    ( r'/problems/', include( 'codechecker.contests.problems' ) ),
    ( r'/submissions/', include( 'codechecker.contests.submissions' ) ),
    ( r'/my-submissions/', include( 'codechecker.contests.submissions' ) ),

 )
