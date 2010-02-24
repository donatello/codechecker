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

def ranklist_cmp(userA, userB):
    if userA[1] != userB[1]:
        return userB[1] - userA[1]
    return userA[2] - userB[2]

"""
Ranklist Algorithm:

We consider only submissions during a contest for problems in that
contest for the ranklist. The SCORE for each user is the sum of scores
for all problems. The score for a problem is full points if it is ACC
and 0 otherwise. The PENALTY for a user is the sum of the penalties
for each problem.  The penalty for a problem is 0 if the problem has
not been solved. If the problem is solved, the penalty is the number
minutes since the start of the contest when the first ACC solution
submitted, with an additional 20 minutes penalty for each unsuccessful
submission for that problem.

The ranklist is simply got by sorting the users with SCORE descending
and PENALTY ascending.

TODO: There is currently a small bug in the ranklist implementation
below. If a user resubmits a problem that is already solved during the
contest, it will add points in the ranklist. This bug has to be fixed!
"""    
def show_ranklist(request, contest):
    vars = { }
    vars['category'] = 'Ranklist'

    problems =  Problem.objects.filter(contest=contest).values( 'pk', 'problemCode', 'maxScore' )

    # form the column headers of the ranklist
    vars['columns'] = [{'name' : 'Team'}, {'name' : 'Total Score'}, {'name' : 'Penalty'}]
    for problem in problems:
        vars['columns'].append( { 'name' : problem['problemCode']
                                  #, 'link' : '/site/problems/' + str(problem['pk']) +'/' 
                                  })

    # first get all submissions that correspond to this contest and
    # are submitted during the duration of this contest
    subs = Submission.objects.filter(submissionTime__gte=contest.startDateTime
                                     ).filter(submissionTime__lte=contest.endDateTime
                                              ).filter(problem__contest__exact = contest.id)

    # form (user -> solved problems), (user -> total scores) and (user ->
    # penalty) mappings.
    user_solvedprobs = {}    
    user_scores = {}
    user_penalty = {}
    for sub in subs:
        # insert user into score mapping with 0 points first.
        if not(sub.user_id in user_scores):
            user_scores[sub.user_id] = 0
        # insert user into penalty mapping with 0 penalty first.
        if not(sub.user_id in user_penalty):
            user_penalty[sub.user_id] = 0
        # insert user into solvedprobs mapping with empty set first.
        if not(sub.user_id in user_solvedprobs):
            user_solvedprobs[sub.user_id] = set([])
        
        # add submission points
        user_scores[sub.user_id] += sub.submissionPoints
        # add solved problem into solvedprobs mapping.
        if sub.result == 'ACC':
            user_solvedprobs[sub.user_id].add(sub.problem_id)

    # now accumulate penalties for solved problems only.
    for sub in subs:
        if sub.problem_id in user_solvedprobs[sub.user_id]:
            user_penalty[sub.user_id] += sub.submissionPenalty

    # now sort the users according to the ranking ordering -> sort by
    # scores descending, and break ties by penalties ascending.
    distinct_users = user_scores.keys()
    user_tuples = []
    for user in distinct_users:
        u = int(user)
        score, penalty = int(user_scores[u]),int(user_penalty[u])
        user_tuples.append([u, score, penalty])
        
    sorted_users = sorted(user_tuples, ranklist_cmp)

    # now form the remaining rows of the ranklist
    rows = []
    for user in sorted_users:
        rowItem = []
        rowItem.append( { 'value': User.objects.get(id = user[0]).username})
        rowItem.append( { 'value': user_scores[user[0]] })
        rowItem.append( { 'value': user_penalty[user[0]] })
        for problem in problems:
            attempts = subs.filter(problem = problem['pk']).filter(user = user[0])
            if problem['pk'] in user_solvedprobs[user[0]]:
                rowItem.append( { 'value': 'ACC (' + str(len(attempts)) + ')'})
            elif len(attempts) != 0:
                rowItem.append( { 'value': '(-' + str(len(attempts)) + ')'})
            else:
                rowItem.append( { 'value': '--'})
        rows.append({'items': rowItem})

    vars['rows'] = rows

    return vars    

# This is my Ranklist view, Didn't want to disturb aditya's logic, so branched out  
# THIS IS COMPLETLY UNTESTED CODE  
def generate_rank_list(request, contest_id):
    # Get All the problems for this contest 
    problems = Problems.objects.filter(contest=contest_id).order_by('problem_code')
    
    # Get all the submissions for this contest
    submissions = Submission.objects.filter(submissionTime__gte=contest.startDateTime
                                     ).filter(submissionTime__lte=contest.endDateTime
                                              ).filter(problem__contest = contest.id)
                                              
    # Get All the Users Participated in this Contest 
    #This is why I love Python List Comprehensions
    users = Set([ submission.user for submission in submissions])
    
    users_list = [ ]
    for user in users :
        user_submissions = submissions.filter(user=user.id)
        user_points = []
        for problem in problems :
              problem_submissions = user_submissions.filter(problem=problem.pk)
              first_accepted = problem_submissions.filter(result='ACC').order_by('submissionTime')[0]
              if first_accepted :
                penalizable = problem_submissions.filter(submissionTime_lte=first_accepted.submissionTime)
              else :
                penalizable = problem_submissions
              
              #calculate the points and penalty here
              points = 0
              penalty = 0
              
              #append the points,penalty tuple to user points
              user_points.append((points, penalty))
              
        #append the sum of points and penalty tuple
        user_points.append( (sum(x),sum(y)) for (x,y) in user_points )
        users_list.append(user_points)
    
    # sort the ranking list that has just been obtained
    sort(users_list, rankingCmp)
    
    #Generate rows and colums now 
    
    #return Context now 
     
     
def contest_view_handle(request, contest_id, action='description'):
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
   
    else :    
        if action == 'ranklist':
            ranklist_vars =  show_ranklist(request, contest)
            vars.update(ranklist_vars)

    context = Context(request, vars)
    template = loader.get_template('contest.html')
    return HttpResponse(template.render(context))

def problem_view_handle(request, problem_id, action='view'):
    vars = { }
    # Get the respective Problem and the contest 
    problem = Problem.objects.get(pk=problem_id)
    contest = problem.contest
    
    current_time = datetime.datetime.now() + offset

    # If the person is not admin and if the contest has not begun, dont show the problem
    if current_time < contest.startDateTime:       
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
                        submissionCode = form.cleaned_data['SubmissionCode'])
                submission.save()
                return HttpResponseRedirect('/site/submissions/')

            
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

    if request.path.find("my_submissions") != -1 or user_context != None :
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

