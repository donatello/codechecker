from django.contrib import admin
from django.db import models
from django.contrib.auth.models import User
from django import forms

# Current Language types that are supported
LANG_TYPES = (
    ('c','C'),
    ('cpp','C++'),
    ('py','PYTHON 2.6.4'),
    #(3,'JAVA'),
)

# Submission Statuses
RESULT_TYPES = (
    ('QU', 'QUEUED'),
    ('CMP', 'COMPILING'),
    ('CMPE', 'COMPILATION FAILURE'),
    ('RUN', 'RUNNING'),
    ('ACC', 'ACCEPTED'),
    ('WA', 'WRONG ANSWER'),
    ('TLE', 'TIME LIMIT EXCEEDED'),
    ('OUTE', 'OUTPUT LIMIT EXCEEDED'),
    ('SEG', 'SEGMENTATION FAULT'),
    ('FPE', 'FLOATING POINT ERROR'),
    ('KILL', 'KILLED'),    
    ('ABRT', 'ABORT SIGNALLED'),    
    ('RTE', 'RUN TIME ERROR'),
    ('WTF', 'NON ZERO RETURN STATUS'),
)

# The site is organized as contests, this is a basic contest model
# Contest has a title,  a general description startTime and endTime.
# Also if it will be publicly viewable by non admins if public is True.

class Contest(models.Model):
    title = models.CharField(max_length = 25) 
    description = models.TextField()
    startTime = models.DateTimeField()
    endTime = models.DateTimeField()
    public = models.BooleanField(default = False)

    def __unicode__(self):
        return self.title

# Each Contest has one or more problems. Orphan or non contest problem are added  
# to a global contest. Each problem has a problem code, statement, constraint 
# notes, sample input and output, time limit, memory limit, maximum score for 
# that problem, allowed Languages for submission to that problem and a penalty 
# for a wrong submission.

class Problem(models.Model):
    contest = models.ForeignKey(Contest)
    pcode = models.CharField(max_length = 25)
    statement = models.TextField()
    notes = models.TextField()
    sampleInput = models.TextField()
    sampleOutput = models.TextField()
    tlimit = models.IntegerField()
    mlimit = models.IntegerField()
    allowedLangs = models.CommaSeparatedIntegerField(max_length=10)
    penalty = models.IntegerField()

    def __unicode__(self):
        return self.pcode
        
# Each problem has several TestSet. A Test set is a set of tests a submission 
# for that problem has to pass to get some score assigned to that TestSet. 
# Testset belongs to a problem and has points.

class TestSet(models.Model):
    problem = models.ForeignKey(Problem)
    points = models.IntegerField()
    
    def __unicode__(self):
        return str(problem) + '-' + str(points)

# Each TestSet has Testcases, which is an atomic test for a submission. It has 
# an input and an corresponding Judge output to that.

class Testcase(models.Model):
    testSet = models.ForeignKey(TestSet)
    input = models.TextField()
    output = models.TextField()

    def __unicode__(self):
        return str(testSet)

# Users can submit their solution to a problem. A submission has a result, time 
# of submission, penalty for that submission, points for the submission, 
# submitted code and any error message that were generated for the submission 
# during the evaluation of the submission
class Submission(models.Model):
    user = models.ForeignKey(User)
    problem = models.ForeignKey(Problem)
    result = models.CharField(max_length=4, choices=RESULT_TYPES, default="QU")
    time = models.DateTimeField()
    language = models.CharField(max_length=10, choices=LANG_TYPES)
    penalty = models.IntegerField(default=0)
    points = models.IntegerField(default=0)
    code = models.TextField()    
    errors = models.TextField()
    
    def __unicode__(self):
        return repr(self.pk)   

# This table logs the result of the evaluation of a submission against
# a testcase. It is to be used in the scoring module for a submission
# to aggregate the results of each testcase.
class TestCaseEval(models.Model):
    submission = models.ForeignKey(Submission)
    testcase = models.ForeignKey(Testcase)
    # memusage is in kilobytes
    mem_usage = models.IntegerField(default=0) 
    # cputime is the total time in seconds (float - microsecond
    # precision).
    cpu_time = models.FloatField(default=0)
    # submission score for this (submission,testcase) pair
    score = models.IntegerField(default=0)
    # submission misc info
    misc_info = models.TextField()
