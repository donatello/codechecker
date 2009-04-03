from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.template import Context,loader
from django import forms
from django.forms import ModelForm
from datetime import datetime
import string,time
from checker.contests.models import Contest,Problem,Submission
from django.contrib.auth.models import User

class RegistrationForm(forms.Form):
    username = forms.CharField(max_length=50,required=True)
    email = forms.EmailField(required=True)
    password =  forms.CharField(label=(u'Password'),widget=forms.PasswordInput(render_value=False)) 
    repeat = password =  forms.CharField(label=(u'Password2'),widget=forms.PasswordInput(render_value=False)) 
    
def register(request):
    c = {}
    if request.method == 'POST' :
        c['form'] = RegistrationForm(request.POST)
        if c['form'].is_valid() :
            user = None
            if (User.objects.get(username__exact=request.POST.username) != None) :
                c['error'] = 'User Already exists'
                c['form'] = RegistrationForm()
            elif (User.objects.get(username__exact=request.POST.email) != None) :
                c['error'] = 'Email Address has been already used'
                c['form'] = RegistrationForm()
            elif (request.POST.password != request.POST.repeat ) :
                c['error'] = 'The passwords do not match'
                c['form'] = RegistrationForm()
            else :
                user = User(username=request.POST.username,
                            email = request.POST.email,
                            password = request.POST.password,
                            is_active = True,
                            is_staff = False,
                            is_superuser = False,)
                user.groups.add('coders')
                user.save()
                login(request,user)
                return HttpResponseRedirect('/csurf/problems/')
    else :
        c['form'] = RegistrationForm()
    
    template = loader.get_template('registration/registration.html')
    context = Context(c)
    return HttpResponse(template.render(context))
    
            
