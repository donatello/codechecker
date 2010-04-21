from models import *

class ContestAdmin(admin.ModelAdmin):
    list_display = ( 'title' , 'startTime', 'endTime' )
    search_fields = ['title']

class ProblemAdmin(admin.ModelAdmin):
    list_display = ( 'pcode', 'contest', 'is_approximate', 'cust_eval', 'cust_minScore', 
                     'cust_maxScore', 'statement', 'constraints', 'sampleInput', 'sampleOutput',
                     'scoring_info', 'tlimit', 'mlimit', 'allowedLangs', 'source_limit') 
    search_fields = ['pcode', 'contest']

class SubmissionAdmin(admin.ModelAdmin):
    list_display = ( 'pk', 'user', 'problem', 'result', 'score', 'time', 'language', 
                     'score', 'code', 'errors') 
    search_fields = [ 'pk', 'user', 'problem', 'result', ] 

class TestSetAdmin(admin.ModelAdmin):
    list_display = ('pk', 'problem', 'maxScore')
    search_fields = ['problem', 'maxScore']
    
class TestcaseAdmin(admin.ModelAdmin):
    list_display = ('pk', 'testSet', 'input', 'output')

admin.site.register(Contest, ContestAdmin)
admin.site.register(Problem, ProblemAdmin)
admin.site.register(Submission, SubmissionAdmin)
admin.site.register(TestSet, TestSetAdmin)
admin.site.register(Testcase, TestCaseAdmin)

