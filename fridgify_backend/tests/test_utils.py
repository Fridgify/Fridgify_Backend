"""Test Utilities"""
# pylint: disable=no-member

import datetime

from django.utils import timezone

from fridgify_backend.models.users import Users
from fridgify_backend.models.fridges import Fridges
from fridgify_backend.models.user_fridge import UserFridge
from fridgify_backend.models.accesstokens import Accesstokens
from fridgify_backend.models.stores import Stores
from fridgify_backend.models.providers import Providers
from fridgify_backend.models.items import Items
from fridgify_backend.models.fridge_content import FridgeContent
from fridgify_backend.utils import const


def setup():
    """Initial setup of DB"""
    # Create A Store
    Stores.objects.create(name="Rewe")
    # Create Providers
    Providers.objects.create(name="Fridgify")
    Providers.objects.create(name="Fridgify-API")
    Providers.objects.create(name="Fridgify-Join")


def clean():
    """Clean all tables"""
    Users.objects.all().delete()
    Fridges.objects.all().delete()
    UserFridge.objects.all().delete()
    Accesstokens.objects.all().delete()
    Items.objects.all().delete()
    FridgeContent.objects.all().delete()


def create_dummyuser(username="dummy_name", name="Dummy", surname="Name", email="dummy@d.de"):
    """Create a user"""
    user = Users()
    user.username = username
    user.name = name
    user.surname = surname
    user.email = email
    # encrypted password - password
    user.password = "$2b$12$1hKYhKg4AU54eyES8qjRYOjInIgObjn0JJ8SlWPOpR9MzKcseMDVS"
    user.birth_date = datetime.date(2000, 10, 17)
    user.save()

    return user


def create_dummyfridge(name="Dummy Fridge"):
    """Create a fridge"""
    fridge = Fridges()
    fridge.name = name
    fridge.description = "This is a dummy fridge"
    fridge.save()

    return fridge


def connect_fridge_user(
        username="dummy_name",
        fridge="Dummy Fridge",
        role=const.Constants.ROLE_USER
):
    """Add user to fridge"""
    user_fridges = UserFridge()
    user_fridges.user = Users.objects.filter(username=username).first()
    user_fridges.fridge = Fridges.objects.filter(name=fridge).first()
    user_fridges.role = role
    user_fridges.save()


def create_login_token(valid_till, username="dummy_name"):
    """Create a login token for a user"""
    token = Accesstokens()
    token.accesstoken = "LoginToken"
    token.valid_till = valid_till
    token.provider = Providers.objects.filter(name="Fridgify").first()
    token.user = Users.objects.filter(username=username).first()
    token.save()


def create_api_token(valid_till, tok="APIToken", username="dummy_name"):
    """Create an API token for a user"""
    token = Accesstokens()
    token.accesstoken = tok
    token.valid_till = valid_till
    token.provider = Providers.objects.filter(name="Fridgify-API").first()
    token.user = Users.objects.get(username=username)
    token.save()


def create_join_token(tok="APIToken", username="dummy_name", fridge=None, valid_till=None):
    """Create a Join token for a user"""
    token = Accesstokens()
    token.accesstoken = tok
    token.valid_till = (
        timezone.now() + timezone.timedelta(hours=12) if valid_till is None else valid_till
    )
    token.provider = Providers.objects.filter(name="Fridgify-Join").first()
    token.user = Users.objects.get(username=username)
    token.fridge = fridge
    token.save()


def create_message_token(
        tok="MessageToken",
        username="dummy_name",
        provider="Fridgify-Notifications",
        valid_till=None
):
    """Create a Join token for a user"""
    token = Accesstokens()
    token.accesstoken = tok
    token.valid_till = (
        timezone.now() + timezone.timedelta(hours=12) if valid_till is None else valid_till
    )
    token.provider = Providers.objects.filter(name=provider).first()
    token.user = Users.objects.get(username=username)
    token.save()


def create_items(name="Item A"):
    """Create items"""
    obj = Items.objects.create(
        name=name,
        description="Description",
        barcode="Barcode123",
        store=Stores.objects.filter(name="Rewe").first()
    )
    return obj


def get_fridge(name):
    """Get a fridge"""
    return Fridges.objects.filter(name=name)


def get_user(name):
    """Get a user"""
    return Users.objects.filter(username=name)


def get_item(name):
    """Get an item"""
    return Items.objects.filter(name=name)


def get_fridge_items(fridge):
    """Get fridge items"""
    return FridgeContent.objects.filter(fridge_id=fridge)


def create_fridge_content(item_id, fridge_id, year=2019, month=12, day=12):
    """Create fridge content"""
    content = FridgeContent.objects.create(
        fridge_id=fridge_id,
        item_id=item_id,
        expiration_date=datetime.date(year, month, day),
        amount=50,
        unit="g"
    )
    return content


def fill_fridges(fridges):
    """Fill fridges"""
    items = []
    store = Stores()
    store.name = "REWE"
    store.save()
    for i in range(0, 5):
        item = Items()
        item.name = "item No. {}".format(i)
        item.description = "sdnjanddkjandakjd"
        item.store = store
        item.save()
        items.append(item)

    for fridge in fridges:
        for j in range(0, 5):
            fridge_content = FridgeContent()
            fridge_content.item = items[j]
            fridge_content.fridge = fridge
            fridge_content.amount = 42
            fridge_content.created_at = timezone.now()
            fridge_content.expiration_date = timezone.now() + timezone.timedelta(days=69)
            fridge_content.unit = "t"
            fridge_content.last_updated = timezone.now()
            fridge_content.save()
