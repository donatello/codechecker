#If the code is not self explanatory in any part of the code, let me know ;) 
from django.contrib import admin

from django.db import models
from django.contrib.auth.models import User
import datetime


LANG_TYPES = (
    (1,'C'),
    (2,'C++'),
    (3,'JAVA'),
)

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
    submissionTime = models.DateTimeField(default=datetime.datetime.now())
    submissionLang = models.SmallIntegerField(choices=LANG_TYPES)
    submissionPenalty = models.IntegerField()
    submissionPoints = models.IntegerField()
    submissionCode = models.TextField()
    
    def __unicode__(self):
        return self.pk

class TestCase(models.Model):
    problem = models.ForeignKey(Problem)
    inputFile = models.TextField()
    outputFile = models.TextField()
    
    def __unicode__(self):
        testCase = 'problem' + repr(self.pk)
        return testCase

    

