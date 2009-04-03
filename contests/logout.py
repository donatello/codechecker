from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth import logout
from django.template import Context,loader
import string
from checker.contests.models import Contest,Problem,Submission,LANG_TYPES
import time
import django.contrib.auth.views 
from django.contrib.auth.models import User

def handle(request):
    logout(request)	
    return HttpResponseRedirect('/csurf/')
    
def password_change(request):
    return django.contrib.auth.views.password_change(request,post_change_redirect='/csurf/',template_name='registration/password_change_form.html')
    

def accounts(request):
    c= { }
    c['show'] = False
    if request.user.is_authenticated() :
        c['show'] = True
        
        user_inst = User.objects.get(username=request.user)
        c['submissions'] = Submission.objects.filter(user=user_inst)
        
    template = loader.get_template('accounts.html')
    context = Context(c)        
    return HttpResponse(template.render(context))
