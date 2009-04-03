from django.http import HttpResponse
from django.template import Context,loader
import string

# Create your views here.

def disp_info(result):
    html = 'hello world'
    return HttpResponse(html)

def default_view(request):
    t = loader.get_template('index.html')
    c = Context()
    return HttpResponse(t.render(c))

