from django.http import HttpResponse


def hello_world(request):
    return HttpResponse("This is the login request page")
