import datetime
from Fridgify_Backend.models.users import Users
from Fridgify_Backend.models.fridges import Fridges
from Fridgify_Backend.models.user_fridge import UserFridge


def create_dummyuser():
    user = Users()
    user.username = "dummy_name"
    user.name = "Dummy"
    user.surname = "Name"
    user.email = "dummy@d.de"
    # encrypted password - password
    user.password = "$2b$12$1hKYhKg4AU54eyES8qjRYOjInIgObjn0JJ8SlWPOpR9MzKcseMDVS"
    user.birth_date = datetime.date(2000, 10, 17)
    user.save()


def create_dummyfridge():
    fridge = Fridges()
    fridge.name = "Dummy Fridge"
    fridge.description = "This is a dummy fridge"
    fridge.save()


def connect_fridge_user():
    user_fridges = UserFridge()
    user_fridges.user = Users.objects.filter(username="dummy_name").first()
    user_fridges.fridge = Fridges.objects.filter(name="Dummy Fridge").first()
    user_fridges.save()
