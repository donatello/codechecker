from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.template import Context,loader
import string,time
from checker.contests.models import Contest,Problem,Submission,LANG_TYPES,Ranklist,Final
from django.conf import settings
from django.contrib.auth.models import User, check_password
from django.shortcuts import render_to_response
from django.core.exceptions import ObjectDoesNotExist



def handle2(request, page):
    c = { }
    page =int(page)
    count = Submission.objects.count() / 25
    submission = Submission.objects.all().order_by('-ID',)[ (page-1)*25 : page*25 ]
    c['prevpage'] = page-1
    c['nextpage'] = page+1
    if page < count + 1:
        c['next'] = True
    if page > 1 :
        c['prev'] = True
		
    c['submission']  = submission
    
       
    template = loader.get_template('status_listing.html')
    context = Context(c)        
    return HttpResponse(template.render(context))

def handle(request):
    return HttpResponseRedirect('/csurf/status/1/')

def sorter(a, b):
    return cmp(a[1][-1],b[1][-1])

def ranklists(request):
    c = {}
    
    users = Ranklist.objects.all().distinct().values('user')
    
    #set the contest id here for displaying the ranklist of that specific contest
    probs = Problem.objects.filter(contest=4)

    rows = { }
    
    c['thead'] = []
    for prob in probs :
        c['thead'].append(str(prob))
    c['thead'].append('TOTAL')
    
    final_rows = []
    final = []    
    for user in users :
        user_inst = User.objects.get(id=user['user'])
        name = user_inst.username
        if name == 'admin':
            continue
        rows[name] = []
        total = 0
        for prob in probs :
            try :
                points = Ranklist.objects.get(user = user_inst , problem = prob).points      
                rows[name].append(points)
                total = total + points
            except ObjectDoesNotExist :
                rows[name].append(0)
            
        #result = Final(user=user_inst,email=user_inst.email,finals_points=total)
        #result.save()
        rows[name].append(total)
        
    items = rows.items()
    items.sort(sorter,reverse=True) 
    
    c['rows'] = items
    
    template = loader.get_template('ranklists.html')
    context = Context(c)        
    return HttpResponse(template.render(context))

def faq(request):
     return render_to_response('faq.html')
