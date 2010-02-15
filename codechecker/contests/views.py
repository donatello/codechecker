from django.http import HttpResponse,HttpResponsePermanentRedirect
from django.template import RequestContext as Context
from django.template import loader

def contests_default(request): 
    return HttpResponsePermanentRedirect("/site/contests/all/")

def show_all_contests(request):
    vars = {}
    vars['category'] = 'Contests'
    vars['contests'] = None 
    template = loader.get_template('table.html')    
    context = Context(request, vars)
    return HttpResponse(template.render(context))

def show_contest(request, contest_id, action="problems"):
    return HttpResponse("<h2> Contest page </h2> Contest Id :" + contest_id + " , Action: " + action)

def show_problem(request):
    return HttpResponse("show_problem")

def show_all_problems(request):
    return HttpResponse("show_all_problems")

def problems_default(request):
    return HttpResponse("problems_default")
