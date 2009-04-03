from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.template import Context,loader
from django import forms
from django.forms import ModelForm
from datetime import datetime
import string
from checker.contests.models import Contest,Problem,Submission
import time


def handle(request,cname):
    c = { }
    
    contest_inst = Contest.objects.get(name=cname)
    
    problems = Problem.objects.filter(contest = contest_inst)

    c['problems']  = problems
    
       
    template = loader.get_template('problem_listing.html')
    context = Context(c)        
    return HttpResponse(template.render(context))

def list_all_problems(request):
    return HttpResponseRedirect('/csurf/problems/page/1/')

def handle_pages(request,page):
    LIMIT = 20
    c = {}
    c['request'] = request
    c['page'] = int(page)
    
    c['pages'] = 1 + int(Problem.objects.count()/LIMIT)
    
    if c['page'] < c['pages']:
        c['next'] = True
    if c['page'] > 1 :
        c['prev'] = True
    
    contests = Contest.objects.filter(is_active=True)
    probs = [ ]
    for cont in contests :
        problems = Problem.objects.filter(contest = cont).values()
        probs = probs.append(problems)   
  
    c['problems'] = probs
    template = loader.get_template('problem_listing.html')
    context = Context(c)        
    return HttpResponse(template.render(context))


class SubmissionForm(ModelForm):
    
    class Meta :
        model = Submission
        fields = ('lang','code',)
    
def view_problem(request,code):
    c = { }
    c['show'] = False
    prob = Problem.objects.get(pcode=code)
    if request.user.is_authenticated():
        c['show'] = True
        inst = Submission(user=request.user, problem=prob, )

        if request.method == 'POST':
            c['form'] = SubmissionForm(request.POST,instance=inst)
            c['form'].save()
            return HttpResponseRedirect('/csurf/status/')
        else :
            c['form'] = SubmissionForm()

    
    c['problem'] = prob
    c['path'] = request.path 
    template = loader.get_template('problem.html')
    context = Context(c)        
    return HttpResponse(template.render(context))
