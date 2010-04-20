from django.template import RequestContext
import django.shortcuts
import datetime
import settings

# This is a wrapper function to render_to_response which will have global variables that needs to be
# passed along with other context variables. Request Context is also passed here
def render_to_response( request, *args, **kwargs ):
    # The base URL
    kwargs['base_url'] = settings.BASE_URL

    #The request context, contains information about the http request
    kwargs['context_instance'] = RequestContext( request )

    # the date time object
    kwargs['server_time'] = datetime.datetime.now()

    return django.shortcuts.render_to_response( request, *args, **kwargs )

# Load the default Home page, About page, References page  
def default( request, action = "base" ):
    template = action + '.html'
    return render_to_response( template, context_instance = RequestContext( request ) )

