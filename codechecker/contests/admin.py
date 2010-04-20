from models import *

class ContestAdmin(admin.ModelAdmin):
    list_display = ( 'title' , 'startTime', 'endTime' )
    search_fields = ['title']

class ProblemAdmin(admin.ModelAdmin):
    list_display = ( 'pcode', 'contest') 
    search_fields = ['pcode', 'contest']

class SubmissionAdmin(admin.ModelAdmin):
    list_display = ( 'pk', 'user', 'problem', 'result', 'points', ) 
    search_fields = [ 'pk', 'user', 'problem', 'result', ] 

class TestSetAdmin(admin.ModelAdmin):
    list_display = ('pk', 'problem', 'points')
    search_fields = ['problem', 'points']
    
class TestCaseAdmin(admin.ModelAdmin):
    list_display = ('pk', 'testSet')

admin.site.register(Contest, ContestAdmin)
admin.site.register(Problem, ProblemAdmin)
admin.site.register(Submission, SubmissionAdmin)
admin.site.register(TestSet, TestSetAdmin)
admin.site.register(Testcase, TestCaseAdmin)

