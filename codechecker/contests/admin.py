from django.db.models import CommaSeparatedIntegerField
import models
from django.contrib import admin
from django import forms

# Admin interface for the Contest Model
class ContestAdmin(admin.ModelAdmin):
    fieldsets = (
        ( 'General', {
            'fields' : ('title','description',)
        }),
        ( 'Schedule', {
            'fields' : ('startTime', 'endTime',)
        }),
        ( 'Status', {
            'fields' : ('public', )
        }),
    )


#Admin interface for the Problem Model
class ProblemAdmin(admin.ModelAdmin):
    
    
    fieldsets = (
        ( 'General', {
            'fields' : ('pcode', 'contest', ),                                
        }),
        ( 'Display', {
            'classes': ('wide'),
            'fields' : ('statement', 'constraints', 'scoring_info', 
                'sampleInput', 'sampleOutput', ),
        }),
        ( 'Scoring', {
            'classes': ('wide'),
            'fields' : ('is_approximate', 'cust_minScore', 'cust_maxScore' , 
                'penalty', ),
        }),
        ( 'Constraints', {
            'classes': ('wide'),
            'fields' : ('tlimit', 'mlimit', 'source_limit', 'allowedLangs', ),
        }),
        ( 'Custom Evaluation', {
            'classes': ('collapse'),
            'fields' : ('cust_eval', ),
            
        }),
    )

#Admin interface for the TestSet Model
class TestSetAdmin(admin.ModelAdmin):
    pass

#Admin interface for the TestcaseAdmin Model
class TestcaseAdmin(admin.ModelAdmin):
    pass

#Admin interface for the Submission Model
class SubmissionAdmin(admin.ModelAdmin):
    pass

#Admin interface for the TestcaseEval Model
class TestCaseEvalAdmin(admin.ModelAdmin):
    pass

# Map all the Admin site with the respective models.
admin.site.register(models.Contest, ContestAdmin)
admin.site.register(models.Problem, ProblemAdmin)
admin.site.register(models.TestSet, TestSetAdmin)
admin.site.register(models.Testcase, TestcaseAdmin)
admin.site.register(models.Submission, SubmissionAdmin)
admin.site.register(models.TestcaseEval, TestCaseEvalAdmin)



