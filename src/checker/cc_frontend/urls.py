from django.conf.urls.defaults import patterns, include
from django.contrib import admin
admin.autodiscover()

import checker.cc_frontend.views as views 

urlpatterns = patterns( '',
    
    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    ( r'^admin/doc/', include( 'django.contrib.admindocs.urls' ) ),

    # Uncomment the next line to enable the admin:
    ( r'^admin/', include( admin.site.urls ) ),

    # Contest App based views
    ( r'^contests/', include( views.contests ) ),
    ( r'^problems/', include( views.problems ) ),
    ( r'^submissions/', include( views.submissions ) ),
    ( r'^my-submissions/', include( views.submissions ) ),

    # default Generic Views
    ( r'^about/$', views.default, { 'action' : 'about'} ),
    ( r'^references/$', views.references, { 'action' : 'references'} ),
    ( r'^$', views.default ),
   
 )
