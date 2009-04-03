from django.http import HttpResponse
from django.template import Context,loader
import string
from checker.contests.models import Contest
import time

def format_time(t):
    ti = time.strptime(str(t),'%Y-%m-%d %H:%M:%S')
    ret = time.strftime('%H:%M %d %b \'%y',ti)    
    return ret


def handle(request):

    c = { }
    # The list of contests is to be displayed 
    contests = Contest.objects.filter(is_active=True).values('name','start_time','end_time')
    
    for item in contests :
        item['start_time'] = format_time(item['start_time'])
        item['end_time'] = format_time(item['end_time'])
            
    c['contests'] = contests

    template = loader.get_template('contest_listing.html')
    context = Context(c)        
    return HttpResponse(template.render(context))

