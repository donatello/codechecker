from django.http import HttpResponse
from django.template import RequestContext as Context
from django.template import loader

def default(request, action='base'):
    template = loader.get_template('base.html')
    context = Context(request)
    return HttpResponse(template.render(context))
