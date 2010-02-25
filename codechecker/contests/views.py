from django.http import HttpResponse, HttpResponseRedirect, HttpResponsePermanentRedirect
from django.template import RequestContext as Context, loader
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import authenticate, login
import time, datetime

from codechecker.contests.models import *
from codechecker.generic_views import debug
    
CONTEST_NOT_BEGUN = "The contest has not begun yet. Please revisit once the contest has started."
offset = datetime.timedelta(hours=5, minutes=30)

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


def rankingComparision( userA, userB ):
    if userA[1] != userB[1]:
        return userB[1] - userA[1]

    return userA[2] - userB[2]
    
def generate_ranklist(request, contest):
    vars = {}

    # Get the contest instance
    contest = Contest.objects.get(pk=contest.id)
    
    # Get All the problems for this contest 
    problems = Problem.objects.filter(contest=contest.id).order_by('problemCode')
    
    #header for the ranklist
    vars['columns'] = [{'name' : 'Team'}, {'name' : 'Total Score'}, {'name' : 'Penalty'}]
    for problem in problems:
        vars['columns'].append( { 'name' : problem.problemCode  })


    # Get all the submissions for this contest
    submissions = Submission.objects.filter(submissionTime__gte=contest.startDateTime
                                 ).filter(submissionTime__lte=contest.endDateTime
                                          ).filter(problem__contest = contest.id)
    users = set([ submission.user for submission in submissions])
    users_list = [ ]
    for user in users :
        # get all the submission for this user
        user_submissions = submissions.filter(user=user.id)
        points = 0
        penalty = 0
        for problem in problems :
            # get all the user submissions for this problem
            problem_submissions = user_submissions.filter(problem=problem.pk)   

            try :
                # get the first accepted submission
                first_accepted = problem_submissions.filter(result='ACC'
                                                            ).order_by('submissionTime')[0]

            except:
                first_accepted = None

            if first_accepted != None:
                penalizable = problem_submissions.filter(submissionTime__lte = 
                                                         first_accepted.submissionTime)
                for sub in penalizable:
                    penalty += sub.submissionPenalty

                points += first_accepted.submissionPoints

        user_tuple = [user, int(points), int(penalty)]            
        users_list.append(user_tuple) 

    users_list = sorted(users_list, rankingComparision)

    # now form the remaining rows of the ranklist
    rows = []
    for item in users_list:
        rowItem = []

        rowItem.append( { 'value': item[0].username})
        rowItem.append( { 'value': item[1] })
        rowItem.append( { 'value': item[2] })

        for problem in problems:
            attempts = submissions.filter(problem = problem.pk).filter(user = item[0])
            solved = attempts.filter(result = 'ACC')

            if len(solved) > 0:
                rowItem.append( { 'value': 'ACC (' + str(len(attempts)) + ')'})
            elif len(attempts) != 0:
                rowItem.append( { 'value': '(-' + str(len(attempts)) + ')'})
            else:
                rowItem.append( { 'value': '--'})

        rows.append({'items': rowItem})

    vars['rows'] = rows      
    
    return vars  
     
def contest_view_handle(request, contest_id, action='description', page=1):
    vars = {}
    
    # Get the respective Contest
    contest = Contest.objects.get(pk=contest_id)
    
     #Get the Current Time 
    current_time = datetime.datetime.now() + offset
    
    vars['title'] = contest.title
    vars['contest'] = contest.pk
    vars['section'] = action
    
    if action == 'description':
        vars['description'] = contest.description
    
    elif action == 'problems' :
        problem_vars =  show_all_problems(request, contest)
        vars.update(problem_vars)
    
        # If the person is not admin and if the contest has not begun,
        # dont show the problem
        if (not request.user.is_superuser) and current_time < contest.startDateTime:            
            vars['errors'] = CONTEST_NOT_BEGUN
   
    elif action == 'ranklist':
        ranklist_vars =  generate_ranklist(request, contest)
        vars.update(ranklist_vars)
        
    elif action == 'submissions':
        submissions_vars = submissions_view_handle(request, contest_id = contest.pk, non_page = True, page=page)
        vars.update(submissions_vars)
        
    elif action == "my_submissions":
        mysub_vars = submissions_view_handle(request, contest_id = contest.pk, user_context = True, non_page = True, page=page)
        vars.update(mysub_vars)
            


    context = Context(request, vars)
    template = loader.get_template('contest.html')
    return HttpResponse(template.render(context))

def problem_view_handle(request, problem_id, action='view', page=1):
    vars = { }
    # Get the respective Problem and the contest 
    problem = Problem.objects.get(pk=problem_id)
    contest = problem.contest
    
    current_time = datetime.datetime.now() + offset

    # If the person is not admin and if the contest has not begun, dont show the problem
    if (not request.user.is_superuser) and current_time < contest.startDateTime:       
        vars['errors'] = CONTEST_NOT_BEGUN
        vars['problem_code'] = problem.problemCode
        vars['section'] = action
        vars['problem'] = problem.pk
    else :
        # Get all the problem parameters 
        vars['problem'] = problem.pk
        vars['problem_code'] = problem.problemCode
        vars['section'] = action
        vars['problem_statement'] = problem.problemStatement
        vars['problem_notes'] = problem.problemNotes
        vars['input_data'] = problem.inputData
        vars['output_data'] = problem.outputData
        vars['tlimit'] = problem.tlimit
        vars['mlimit'] = problem.mlimit
        
        elif action == 'submissions':
            submissions_vars = submissions_view_handle(request, problem_id = problem.pk, non_page = True, page=page)
            vars.update(submissions_vars)
        
        elif action == "my_submissions":
            mysub_vars = submissions_view_handle(request, problem_id = problem.pk, user_context = True, non_page = True, page=page)
            vars.update(mysub_vars)

    context = Context(request, vars)
    template = loader.get_template('problem.html')
    return HttpResponse(template.render(context))

@login_required(redirect_field_name='next')
def problem_submit(request, problem_id) :
    vars = {}
     # Get the respective Problem and the contest 
    problem = Problem.objects.get(pk=problem_id)
    contest = problem.contest
    
    #Get the Current Time 
    current_time = datetime.datetime.now() + offset
    
    vars['problem'] = problem.pk
    vars['problem_code'] = problem.problemCode
    vars['section'] = 'submit'
    
    if (not request.user.is_superuser) and current_time < contest.startDateTime :
        vars['errors'] = CONTEST_NOT_BEGUN
    else :
        if request.method == 'POST' :
            form = SubmissionForm(request.POST)
            if form.is_valid():
                submission = Submission( problem = problem , 
                                         user = request.user, 
                                         submissionLang = form.cleaned_data['SubmissionLang'], 
                                         submissionCode = form.cleaned_data['SubmissionCode'],
                                         submissionTime = current_time)
                submission.save()
                return HttpResponseRedirect('/site/submissions/')

            
        vars['form'] = SubmissionForm()

    context = Context(request, vars)
    template = loader.get_template('problem.html')
    return HttpResponse(template.render(context))

def submissions_view_handle(request, contest_id = None, problem_id = None, user_context = None, non_page=None, page = 1):
    vars = {}
    vars['category'] = 'Submissions'
    vars['colored'] = True 
    base_url = '/site/'
    if contest_id != None :
        base_url = base_url + 'contests/' + str(contest_id) + '/'
        all_submissions = Submission.objects.order_by('-pk').filter(problem__contest = contest_id)
    elif problem_id != None :
        base_url = base_url + 'problems/' + str(problem_id) + '/'
        all_submissions = Submission.objects.order_by('-pk').filter(problem=problem_id)
    else :
        all_submissions = Submission.objects.order_by('-pk').all()

    base_url = base_url + 'submissions'
    vars['base_url'] = base_url    

    if request.path.find("my_submissions") != -1 or user_context != None :
        if not request.user.is_authenticated() :
            return HttpResponseRedirect('/site/login/?next=' + request.path)
        all_submissions = all_submissions.filter(user=request.user)

    paginator = Paginator(all_submissions, 15) 
    
    try :
        submissions_page = paginator.page(page)
    except (EmptyPage, InvalidPage):
        submissions_page = paginator.page(paginator.num_pages)
    
    submissions = submissions_page.object_list

    vars['submissions_page'] = submissions_page

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
    
    if non_page:
        return vars
    context = Context(request, vars)
    template = loader.get_template('table.html')
    return HttpResponse(template.render(context))

