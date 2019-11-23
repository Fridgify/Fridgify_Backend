import datetime
from Fridgify_Backend.models.users import Users
from Fridgify_Backend.models.providers import Providers


def create_dummyuser():
    user = Users()
    user.username = "dummy_name"
    user.name = "Dummy"
    user.surname = "Name"
    user.email = "dummy@d.de"
    # encrypted password
    user.password = "$2b$12$1hKYhKg4AU54eyES8qjRYOjInIgObjn0JJ8SlWPOpR9MzKcseMDVS"
    user.birth_date = datetime.date(2000, 10, 17)
    user.save()


def create_providers():
    Providers.objects.create(name="Fridgify")
    Providers.objects.create(name="Fridgify-API")