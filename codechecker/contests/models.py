from django.db import models
from django.contrib.auth.models import User


# Current Language types that are supported
LANG_TYPES = ( 
    ( 'c', 'C' ),
    ( 'cpp', 'C++' ),
    ( 'py', 'PYTHON 2.6.4' ),
    #(3,'JAVA'),
 )

# Submission Statuses
RESULT_TYPES = ( 
    ( 'QU', 'QUEUED' ),
    ( 'CMP', 'COMPILING' ),
    ( 'CMPE', 'COMPILATION FAILURE' ),
    ( 'RUN', 'RUNNING' ),
    ( 'ACC', 'ACCEPTED' ),
    ( 'WA', 'WRONG ANSWER' ),
    ( 'TLE', 'TIME LIMIT EXCEEDED' ),
    ( 'OUTE', 'OUTPUT LIMIT EXCEEDED' ),
    ( 'SEG', 'SEGMENTATION FAULT' ),
    ( 'FPE', 'FLOATING POINT ERROR' ),
    ( 'KILL', 'KILLED' ),
    ( 'ABRT', 'ABORT SIGNALLED' ),
    ( 'RTE', 'RUN TIME ERROR' ),
    ( 'WTF', 'NON ZERO RETURN STATUS' ),
 )

# The site is organized as contests, this is a basic contest model
# Contest has a title,  a general description startTime and endTime.
# Also if it will be publicly viewable by non admins if public is True.

class Contest( models.Model ):
    title = models.CharField( max_length = 25 )
    description = models.TextField()
    startTime = models.DateTimeField()
    endTime = models.DateTimeField()
    public = models.BooleanField( default = False )

    def __unicode__( self ):
        return self.title

# Each Contest has one or more problems. Orphan or non contest problem are added  
# to a global contest. Each problem has a problem code, statement, constraint 
# notes, sample input and output, time limit, memory limit, maximum score for 
# that problem, allowed Languages for submission to that problem and a penalty 
# for a wrong submission.

class Problem( models.Model ):

    #Problem related metadata fields follow
    contest = models.ForeignKey( Contest )
    pcode = models.CharField( max_length = 25 )
    penalty = models.IntegerField()
    is_approximate = models.BooleanField( default = False )
    cust_eval = models.FileField( upload_to = "/tmp", default = None )
    cust_minScore = models.IntegerField( default = 0 )
    cust_maxScore = models.IntegerField( default = 100 )

    #Fields related to the display of the problem statement follow:
    statement = models.TextField()
    constraints = models.TextField() # Info about input constraints.
    sampleInput = models.TextField()
    sampleOutput = models.TextField()

    # Info about how the problem will be scored.
    scoring_info = models.TextField()

    tlimit = models.IntegerField() # (in seconds)
    mlimit = models.IntegerField() # (in MiB)
    allowedLangs = models.CommaSeparatedIntegerField( max_length = 10 )

    # The max source file size allowed for the problem (in KiB).  
    source_limit = models.IntegerField( default = 50 )

    def __unicode__( self ):
        return self.pcode

# Each problem has several TestSet. A Test set is a set of tests a submission 
# for that problem has to pass to get some score assigned to that TestSet. 
# Testset belongs to a problem and has a maximum score.

class TestSet( models.Model ):
    problem = models.ForeignKey( Problem )
    maxScore = models.IntegerField()

    def __unicode__( self ):
        return str( self.problem ) + '-' + str( self.maxScore )

# Each TestSet has Testcases, which is an atomic test for a submission. It has 
# an input and an corresponding Judge output to that.

class Testcase( models.Model ):
    testSet = models.ForeignKey( TestSet )
    input = models.TextField()
    output = models.TextField()

    def __unicode__( self ):
        return str( self.testSet )

# Users can submit their solution to a problem. A submission has a result, time 
# of submission, penalty for that submission, score for the submission, 
# submitted code and any error message that were generated for the submission 
# during the evaluation of the submission
class Submission( models.Model ):
    user = models.ForeignKey( User )
    problem = models.ForeignKey( Problem )
    result = models.CharField( max_length = 4, choices = RESULT_TYPES, default = "QU" )
    time = models.DateTimeField()
    language = models.CharField( max_length = 10, choices = LANG_TYPES )
    penalty = models.IntegerField( default = 0 )
    score = models.IntegerField( default = 0 )
    code = models.TextField()
    errors = models.TextField()

    def __unicode__( self ):
        return repr( self.pk )

# This table logs the result of the evaluation of a submission against
# a testcase. It is to be used in the scoring module for a submission
# to aggregate the results of each testcase.
class TestcaseEval( models.Model ):
    submission = models.ForeignKey( Submission )
    testcase = models.ForeignKey( Testcase )
    # memusage is in kilobytes
    mem_usage = models.IntegerField( default = 0 )
    # cputime is the total time in seconds (float - microsecond
    # precision).
    cpu_time = models.FloatField( default = 0 )
    # submission score for this (submission,testcase) pair
    score = models.IntegerField( default = 0 )
    # pass/fail status
    pass_status = models.CharField( max_length = 10 )
    # submission misc info
    misc_info = models.TextField()
