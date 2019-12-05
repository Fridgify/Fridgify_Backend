import datetime
from Fridgify_Backend.models.users import Users
from Fridgify_Backend.models.fridges import Fridges
from Fridgify_Backend.models.user_fridge import UserFridge
from Fridgify_Backend.models.accesstokens import Accesstokens
from Fridgify_Backend.models.stores import Stores
from Fridgify_Backend.models.providers import Providers
from Fridgify_Backend.models.items import Items
from Fridgify_Backend.models.fridge_content import FridgeContent


def setup():
    # Create A Store
    Stores.objects.create(name="Rewe")
    # Create Providers
    Providers.objects.create(name="Fridgify")
    Providers.objects.create(name="Fridgify-API")


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


def create_login_token(valid_till):
    token = Accesstokens()
    token.accesstoken = "LoginToken"
    token.valid_till = valid_till
    token.provider = Providers.objects.filter(name="Fridgify").first()
    token.user = Users.objects.filter(username="dummy_name").first()
    token.save()


def create_api_token(valid_till):
    token = Accesstokens()
    token.accesstoken = "APIToken"
    token.valid_till = valid_till
    token.provider = Providers.objects.filter(name="Fridgify-API").first()
    token.user = Users.objects.filter(username="dummy_name").first()
    token.save()


def create_items(name):
    if name == "":
        name = "Item A"
    Items.objects.create(name=name, description="Description", store=Stores.objects.filter(name="Rewe").first())
    return Items.objects.filter(name="Item A").first()


def get_fridge(name):
    return Fridges.objects.filter(name=name)


def get_user(name):
    return Users.objects.filter(username=name)


def get_item(name):
    return Items.objects.filter(name=name)


def get_fridge_items(fridge):
    return FridgeContent.objects.filter(fridge_id=fridge)


def create_fridge_content(item_id, fridge_id):
    FridgeContent.objects.create(fridge_id=fridge_id, item_id=item_id, expiration_date=datetime.date(2019, 12, 12),
                                 amount=50, unit="g")
