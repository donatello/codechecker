from django.http import HttpResponse

def default(request):
    return HttpResponse(" <h1> About Page ! </h2> <h3> More to come, soon ! </h3>");
