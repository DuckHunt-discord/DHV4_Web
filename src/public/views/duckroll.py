from django.http import HttpResponsePermanentRedirect


def duckroll(request):
    return HttpResponsePermanentRedirect('https://www.youtube.com/watch?v=HP362ccZBmY')
