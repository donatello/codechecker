from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext as Context, loader

def default(request, action='base'):
    template = loader.get_template(action + ".html")
    context = Context(request)
    return HttpResponse(template.render(context))
