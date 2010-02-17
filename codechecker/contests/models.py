from django.contrib import admin

from django.db import models
from django.contrib.auth.models import User
import datetime


LANG_TYPES = (
    (1,'C'),
    (2,'C++'),
    (3,'JAVA'),
)

RESULT_TYPES = (
    ('QU', 'QUEUED'),
    ('CMP', 'COMPILING'),
    ('RUN', 'RUNNING'),
)

RUNS_PATH = '/share/data/submissions/'

class Contest(models.Model):
    title = models.CharField(max_length = 25)
    description = models.TextField()
    startDateTime = models.DateTimeField()
    endDateTime = models.DateTimeField()

    def __unicode__(self):
        return self.title
    
    
class Team(models.Model):
    name = models.CharField(max_length=25)
    teamSize = models.IntegerField()
    
    def __unicode__(self):
        return self.name

class Problem(models.Model):
    contest = models.ForeignKey(Contest)
    problemCode = models.CharField(max_length = 25)
    problemStatement = models.TextField()
    problemNotes = models.TextField()
    inputData= models.TextField()
    outputData= models.TextField()
    tlimit = models.IntegerField()
    mlimit = models.IntegerField()
    maxScore = models.IntegerField()
    allowableLanguages = models.CommaSeparatedIntegerField(max_length=10)
        
    def __unicode__(self):
        return self.problemCode
        
class Submission(models.Model):
    user = models.ForeignKey(User)
    problem = models.ForeignKey(Problem)
    result = models.CharField(max_length=4, choices=RESULT_TYPES)
    submissionTime = models.DateTimeField(default=datetime.datetime.now())
    submissionLang = models.SmallIntegerField(choices=LANG_TYPES)
    submissionPenalty = models.IntegerField()
    submissionPoints = models.IntegerField()
    submissionCode = models.TextField()    
    
    def __unicode__(self):
        return self.pk

    # The prefix underscore implies that the function is not an
    # exported interface (i think).
    def _generate_compile_command(self):
        s = str('')
        file_root = RUNS_PATH + str(self.pk) 

        if self.get_submissionLang_display() == 'C++':
            s = ('g++  -o ' + str(file_root)  + '.exe ' + 
                 str(str(file_root) + '.' + sub['lang']))

        elif self.get_submissionLang_display() == 'C':
            s = ('gcc  -o ' + str(file_root)  + '.exe ' + 
                 str(str(file_root) + '.' + sub['lang']))

        elif self.get_submissionLang_display() == 'JAVA':
            s = 'do nothing for now '

        return s


    def write_code_to_disk(self):
        f = open(RUNS_PATH + str(self.pk) + '.' + sub_instance.lang,'w')
        f.write(self.submissionCode)
        f.close()

    def compile(self):
        cmd = _generate_compile_command()
        self.result = 'CMP'
        self.save()
        compile_output = os.popen(submission['cmd'])
        return compiler_out.read()
        
    def check_compile_result(self):
        if os.path.exists(RUNS_PATH + str(sub_instance.ID) + '.exe') == 0 :
            sub_instance.result = 'CMPE'
            sub_instance.save()
            return False
        return True
    
    # This method should only be called if self.check_compile_result()
    # returned True
    def execute(self, prob):   
        if prob.ptype == 'Simple' :
            import SimpleChecker # SUREN --> This line wont work
                                 # because of the folder arrangement!
            SimpleChecker.run(self)            
#        elif prob.ptype == 'Multiple' :
#            MultipleChecker.run(self)
#        elif prob.ptype == 'Complex' :
#            ComplexChecker.run(self)


class TestCase(models.Model):
    problem = models.ForeignKey(Problem)
    inputFile = models.TextField()
    outputFile = models.TextField()
    
    def __unicode__(self):
        testCase = 'problem' + repr(self.pk)
        return testCase


