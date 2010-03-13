from models import *

class ContestAdmin(admin.ModelAdmin):
    list_display = ( 'title' , 'startDateTime', 'endDateTime' )
    search_fields = ['title']

class TeamAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ['name',]

class ProblemAdmin(admin.ModelAdmin):
    list_display = ( 'problemCode', 'contest') 
    search_fields = ['problemCode', 'contest']

class SubmissionAdmin(admin.ModelAdmin):
    list_display = ( 'pk', 'user', 'problem', 'result', 'submissionPoints', ) 
    search_fields = [ 'pk', 'user', 'problem', 'result', ] 

class TempRegAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'primary_email')
    search_fields = ['name']

class TestSetAdmin(admin.ModelAdmin):
    list_display = ('pk', 'problem', 'testcase')
    search_fields = ['problem', 'testcase']

