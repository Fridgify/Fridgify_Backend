import django.db

from Fridgify_Backend.models.fridges import Fridges
from Fridgify_Backend.models.user_fridge import UserFridge
from Fridgify_Backend.models.fridge_content import FridgeContent
from Fridgify_Backend.models.items import Items
from Fridgify_Backend.models.stores import Stores


def fridge_add_item(fridge_id, user_id, req_body):
    """
    Add an item to a fridge
    :param fridge_id: Fridge ID
    :param user_id: User ID
    :param req_body: Request Body
    :return: 1 - Creation Success | 0 - User has no access to Fridge | -1 - Creation Failed
    """
    # Check if there is a User Fridge combination
    user_fridges = UserFridge.objects.filter(user_id=user_id, fridge_id=fridge_id)
    print(user_fridges)
    # Get fridge
    fridge = get_fridge(fridge_id)
    len_uf = len(user_fridges)
    if len_uf == 1:
        # Check if item already exists
        item = check_item_exists(req_body["name"], req_body["store"])
        if item == -1:
            # Think about a possible error message
            print("Mistake")
            return -1
        elif item is not None:
            # Create the content with existing item
            try:
                FridgeContent.objects.create(item=item, fridge=fridge, amount=req_body["amount"],
                                             unit=req_body["unit"], expiration_date=req_body["expiration_date"])
            except django.db.IntegrityError:
                return -1
            return 1
        else:
            # Create an item
            item = create_item(req_body)
            if item is not None:
                # Create fridge content with created item
                try:
                    FridgeContent.objects.create(item=item, fridge=fridge, amount=req_body["amount"],
                                                 unit=req_body["unit"], expiration_date=req_body["expiration_date"])
                except django.db.IntegrityError:
                    return -1
                return 1
            else:
                # Error response for failed item creation
                print("Item Creation went wrong")
                return -1
    elif len_uf < 1:
        print("No fridge found")
        return 0
    elif len_uf > 1:
        print("Something went wrong. Seems like there are multiple fridges with the same id for that user")
        return -1


def check_item_exists(name, store):
    """
    Check if an item exists
    :param name: Name of Item
    :param store: Store Name of Store
    :return: Item Instance | -1 - Error: Multiple Items | None - Nothing found
    """
    # Get Items for information in body
    item_obj = Items.objects.filter(name=name, store__name=store)
    if len(item_obj) == 1:
        # Return the Item (as Item instance)
        return item_obj.first()
    elif len(item_obj) > 1:
        # There are multiple items for the same name and store. This should not happen.
        return -1
    else:
        return None


# TODO: Outsource into own file
def create_item(req_body):
    """
    Create an item out of the request body attributes
    :param req_body: Request Body
    :return: Created Item Instance | None - Creation failed
    """
    # Get Store
    store_id = store_exists(req_body["store"])
    if store_id is not None:
        # Create the item
        Items.objects.create(name=req_body["name"], description=req_body["description"], store=store_id)
        # Return the item instance
        return Items.objects.filter(name=req_body["name"], description=req_body["description"],
                                    store=store_id).first()
    return None


# TODO: Outsource into own File
def store_exists(store):
    """
    Returns the store instance for the store name
    :param store: name of store
    :return: Store Instance | None - There is no such store
    """
    # Get Store
    obj_store = Stores.objects.filter(name=store)
    if len(obj_store) < 0:
        return None
    else:
        # Return Store instance
        return obj_store.first()


# TODO: Outsource into own File
def get_fridge(fridge_id):
    """
    Return fridge for fridge id
    :param fridge_id: ID of fridge
    :return: None - there is no fridge | Fridge Instance
    """
    # Get Fridge for fridge id
    obj_fridge = Fridges.objects.filter(fridge_id=fridge_id)
    if len(obj_fridge) == 1:
        # Return Fridge Instance
        return obj_fridge.first()
    else:
        return None
