from django.http import HttpResponse, HttpResponseRedirect, HttpResponsePermanentRedirect
from django.template import RequestContext as Context
from django.template import loader
from codechecker.contests.models import *
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.contrib.auth.decorators import login_required
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

def problems_default(request):
    return HttpResponsePermanentRedirect("/site/problems/all/");

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
        rows.append({ 'items' : rowItem})
    vars['rows'] = rows
    vars['page'] = paginated_contests
    template = loader.get_template('table.html')    
    context = Context(request, vars)
    return HttpResponse(template.render(context))

def show_all_problems(request, contest = -1):
    vars = { }
    vars['category'] = 'Problems'
    vars['columns'] = [{'name' : 'Problem'} , {'name' : 'Maximum Points'}]

    if contest == -1 :
        problems =  Problem.objects.all().values( 'pk', 'contest', 'problemCode', 'maxScore' )
        vars['columns'].append( {'name' : "Contest" })
    else :
        problems =  Problem.objects.filter(contest=contest).values( 'pk', 'problemCode', 'maxScore' )

    rows = []
    for problem in problems :
        rowItem = []
        rowItem.append( { 'link' : '/site/problems/' + str(problem['pk']) +'/', 'value': problem['problemCode'] })
        rowItem.append( { 'value' : problem['maxScore']} )

        if contest == -1 :
            this_contest = Contest.objects.get(pk=problem['contest']) 
            rowItem.append( { 'link' : '/site/contests/' + str(this_contest.pk) +'/', 'value' : this_contest.title } )  

        rows.append({ 'items' :rowItem})
    vars['rows'] = rows

    if contest != -1 :
        return vars

    context = Context(request, vars)
    template = loader.get_template('table.html')
    return HttpResponse(template.render(context))

def contest_view_handle(request, contest_id, action='description'):
    vars = {}
    contest = Contest.objects.get(pk=contest_id)
    vars['contest'] = contest.pk
    vars['section'] = action 
    vars['description'] = contest.description
    vars['title'] = contest.title

    if action == 'problems' :
        problem_vars =  show_all_problems(request, contest)
        vars.update(problem_vars) 

    context = Context(request, vars)
    template = loader.get_template('contest.html')
    return HttpResponse(template.render(context))

def problem_view_handle(request, problem_id, action='view'):
    vars = { }
    problem = Problem.objects.get(pk=problem_id)
    vars['problem'] = problem.pk
    vars['problem_code'] = problem.problemCode
    vars['section'] = action
    vars['problem_statement'] = problem.problemStatement
    vars['problem_notes'] = problem.problemNotes
    vars['input_data'] = problem.inputData
    vars['output_data'] = problem.outputData
    vars['tlimit'] = problem.tlimit
    vars['mlimit'] = problem.mlimit

    context = Context(request, vars)
    template = loader.get_template('problem.html')
    return HttpResponse(template.render(context))

@login_required(redirect_field_name='next')
def problem_submit(request, problem_id) :
    vars = {}
    problem = Problem.objects.get(pk=problem_id)
    if request.method == 'POST' :
        form = SubmissionForm(request.POST)
        if form.is_valid():
            submission = Submission( problem = problem , 
                    user = request.user, 
                    submissionLang = form.cleaned_data['SubmissionLang'], 
                    submissionCode = form.cleaned_data['SubmissionCode'])
            submission.save()
            return HttpResponseRedirect('/site/submissions/')

    vars['problem'] = problem.pk
    vars['problem_code'] = problem.problemCode
    vars['section'] = 'submit'
    vars['form'] = SubmissionForm()

    context = Context(request, vars)
    template = loader.get_template('problem.html')
    return HttpResponse(template.render(context))

def submissions_view_handle(request, contest_id = None, problem_id = None, user_context = None, page = 1, non_page=None ):
    vars = {}
    vars['category'] = 'Submissions'
    vars['colored'] = True 
    if contest_id != None :
        all_submissions = []
        problems = Problem.objects.filter(contest=contest_id)
        for problem in problems :            
            l = Submission.objects.order_by('-pk').filter(problem=problem.pk)
            all_submissions.extend(l)
    elif problem_id != None :
        all_submissions = Submission.objects.order_by('-pk').filter(problem=problem_id)
    else :
        all_submissions = Submission.objects.order_by('-pk').all()

    if request.path.find("my_submissions") != -1 :
        if not request.user.is_authenticated() :
            return HttpResponseRedirect('/site/login/?next=' + request.path)
        all_submissions = all_submissions.filter(user=request.user)

    paginator = Paginator(all_submissions, 25) 
    
    try :
        submissions_page = paginator.page(page)
    except (EmptyPage, InvalidPage):
        submissions_page = paginator.page(paginator.num_pages)

    submissions = submissions_page.object_list
    debug(submissions)
    vars['columns'] = [ {'name' : 'ID'}, {'name': 'Problem'}, {'name': 'User'}, {'name': 'Result'}, {'name': 'Language'}, ] 
    vars['colored'] = True 
    rows = []
    for submission in submissions :
        rowItem = []
        problem = submission.problem
        rowItem.append({ 'value' : str(submission.pk) })
        rowItem.append({ 'link' : '/site/problems/' + str(problem.pk) +'/', 'value' : problem.problemCode })
        rowItem.append({ 'value' : str(submission.user)}) 
        rowItem.append({ 'value' : submission.get_result_display() })
        rowItem.append({ 'value' : submission.get_submissionLang_display() })
        res = submission.result
        if res == "QU" or res == "CMP" or res == "RUN" :
            color = "grey"
        elif res == "ACC" : 
            color = "green"
        else :
            color = "orange"
        rows.append({'items' : rowItem, 'color':color})
    
    vars['rows'] = rows
    if non_page :
        return vars
    context = Context(request, vars)
    template = loader.get_template('table.html')
    return HttpResponse(template.render(context))

