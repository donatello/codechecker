from checker.contests.models import *
from django.contrib import admin

class ContestAdmin(admin.ModelAdmin):
    list_display = ( 'name', 'start_time', 'end_time', 'is_active', )
    search_fields = ['name']

class ProblemAdmin(admin.ModelAdmin):
    list_display = ( 'pcode', 'contest', 'tlimit', 'mlimit', )
    search_fields = ['pcode']

class SubmissionAdmin(admin.ModelAdmin):
    list_display = ( 'ID', 'user', 'problem', 'lang','time', 'result', )
    search_fields = ['user']

class RanklistAdmin(admin.ModelAdmin):
    list_display = ( 'ID', 'user', 'problem', 'submission' ,'points' )
    search_fields = ['user']
    
admin.site.register(Contest,ContestAdmin)
admin.site.register(Problem,ProblemAdmin)
admin.site.register(Submission,SubmissionAdmin)
admin.site.register(Ranklist,RanklistAdmin)
