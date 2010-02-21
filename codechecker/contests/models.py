from django.contrib import admin
from django.db import models
from django.contrib.auth.models import User
from django.forms import ModelForm
import datetime


LANG_TYPES = (
    (1,'C'),
    (2,'C++'),
    (3,'JAVA'),
)

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
    ('UNKN', ''),
    ('WTF', ''),
)

RUNS_PATH = '/tmp/'

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
            s = ('g++  -Wall -o ' + str(file_root)  + '.exe ' + 
                 str(str(file_root) + '.' + self._get_filename_extension()))

        elif self.get_submissionLang_display() == 'C':
            s = ('gcc  -Wall -o ' + str(file_root)  + '.exe ' + 
                 str(str(file_root) + '.' + self._get_filename_extension()))

        elif self.get_submissionLang_display() == 'JAVA':
            s = 'do nothing for now '

        return s

    def _get_filename_extension(self):
        if self.get_submissionLang_display() == 'C++':
            return "cpp"
        elif self.get_submissionLang_display() == 'C':
            return "c"
        elif self.get_submissionLang_display() == 'JAVA':
            return "java"
        else:
            return "c"

    def write_code_to_disk(self):
        f = open(RUNS_PATH + str(self.pk) + '.' + self._get_filename_extension(),'w')
        f.write(self.submissionCode)
        f.close()

    def compile(self):
        import subprocess
        cmd = self._generate_compile_command()
        self.result = 'CMP'
        self.save()
        compile = subprocess.Popen(cmd, shell=True, stderr=subprocess.PIPE)
        compile_out = compile.communicate()[1]
        return compile_out
        
    def check_compile_result(self):
        import os
        if os.path.exists(RUNS_PATH + str(self.pk) + '.exe') == 0:
            self.result = 'CMPE'
            self.save()
            return False
        return True

class SubmissionForm(ModelForm):
    class Meta:
        model = Submission
        fields = [ 'submissionLang', 'submissionCode' ]
        widgets = {
                    'submissionCode' : Textarea(attrs={'cols' : 100, 'rows' : 25}),
                }

class TestCase(models.Model):
    problem = models.ForeignKey(Problem)
    inputFile = models.TextField()
    outputFile = models.TextField()
    
    def __unicode__(self):
        testCase = 'problem' + repr(self.pk)
        return testCase


