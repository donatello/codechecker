from django.http import HttpResponse,HttpResponsePermanentRedirect
from django.template import RequestContext as Context
from django.template import loader
from codechecker.contests.models import *
from django.core.paginator import Paginator, InvalidPage, EmptyPage
import time

def debug(obj):
    import sys
    print >> sys.stderr,'[debug] ' + repr(obj)
    sys.stderr.flush()

def format_time(t):
        ti = time.strptime(str(t),'%Y-%m-%d %H:%M:%S')
        ret = time.strftime('%H:%M %d %b %Y',ti)    
        return ret 

def contests_default(request): 
    return HttpResponsePermanentRedirect('/site/contests/all/')

def show_all_contests(request, page=1):
    vars = {}
    vars['category'] = 'Contests'
    contests =  Contest.objects.all().values( 'pk', 'title', 'startDateTime', 'endDateTime')
    pagination = Paginator(contests, 25)
    try :
        paginated_contests = pagination.page(page)
    except (EmptyPage, InvalidPage):
        paginated_contests = pagination.page(pagination.num_pages)
    
    vars['columns'] = [ {'name' : 'Contest'} , {'name' : 'Start Time'} , {'name': 'End Time'} ]
    
    contests = paginated_contests.object_list

    rows = []
    for contest in contests :
        rowItem = []
        rowItem.append( { 'link' : '/site/contests/' + str(contest['pk']) +'/', 'value': contest['title'] })
        rowItem.append( { 'value' : format_time(contest['startDateTime']) })
        rowItem.append( { 'value' : format_time(contest['endDateTime']) })
        rows.append(rowItem)
    vars['rows'] = rows
    template = loader.get_template('table.html')    
    context = Context(request, vars)
    return HttpResponse(template.render(context))

def show_contest(request, contest_id, action='description'):
    vars = {}
    contest = Contest.objects.get(pk=contest_id)
    vars['contest'] = contest.pk
    vars['section'] = action 
    vars['description'] = contest.description
    vars['title'] = contest.title
    context = Context(request, vars)
    template = loader.get_template('contest.html')
    return HttpResponse(template.render(context))

def show_problem(request):
    return HttpResponse('show_problem')

def show_all_problems(request):
    return HttpResponse('show_all_problems')

def problems_default(request):
    return HttpResponse('problems_default')
