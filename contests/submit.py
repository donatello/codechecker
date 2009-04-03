from django.http import HttpResponse,HttpResponseRedirect
from django.template import Context,loader
from django.contrib.auth.decorators import login_required
import os,string

def handle(request):
    c = { }
    context = Context(c)
    template = loader.get_template('submit.html')
    context = Context(c)        
    return HttpResponse(template.render(context))
