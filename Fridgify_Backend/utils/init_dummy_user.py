import datetime
from django.http import HttpResponse
from django.http import JsonResponse
from Fridgify_Backend.models.users import Users
from Fridgify_Backend.models.providers import Providers


def create_dummyuser(request):
    print(request.method)
    if request.method != "OPTIONS":
        return HttpResponse(status=400, content="Nice try")
    if Providers.objects.filter().exists():
        return HttpResponse(status=400, content="You´re already dumb")
    provider = Providers()
    provider.name = "Fridgify"
    provider.save()
    provider2 = Providers()
    provider2.name = "Fridgify-API"
    provider2.save()
    user = Users()
    user.username = "dummy_name"
    user.name = "Dummy"
    user.surname = "Name"
    user.email = "dummy@d.de"
    # encrypted password
    user.password = "$2b$12$1hKYhKg4AU54eyES8qjRYOjInIgObjn0JJ8SlWPOpR9MzKcseMDVS"
    user.birth_date = datetime.date(2000, 10, 17)
    user.save()
    user2 = Users()
    user2.username = "testUser"
    user2.name = "Test"
    user2.surname = "User"
    user2.email = "test@user.de"
    # encrypted password = password
    user2.password = "$2b$12$1hKYhKg4AU54eyES8qjRYOjInIgObjn0JJ8SlWPOpR9MzKcseMDVS"
    user2.birth_date = datetime.date(2000, 10, 17)
    user2.save()
    return JsonResponse(status=200, data={
        "message": "Users are dummy_name and testUser. Password is password"
    })
