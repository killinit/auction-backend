from django.shortcuts import render_to_response, RequestContext


def index(request):
    return render_to_response("index.html", locals(), context_instance=RequestContext(request))
