from django.http import HttpResponse


def hello_world(request):
    if request.method == 'POST':
        return HttpResponse("This is the login request page")
    else:
        res = HttpResponse(status=405, reason="Method not allowed.")
        res["Allow"] = "POST"
        return res
