from django.utils import timezone
from unittest import mock
from django.test import TestCase, RequestFactory

from Fridgify_Backend.utils import fridge_content_handler
from Fridgify_Backend.models.fridges import Fridges
from Fridgify_Backend.models.users import Users
from Fridgify_Backend.models.fridge_content import FridgeContent
from Fridgify_Backend.models.items import Items
from Fridgify_Backend.tests import test_utils


class UtilsTestCaseFridgeContentHandler(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        test_utils.setup()
        test_utils.create_dummyuser()
        Fridges.objects.create(name="Dummy Fridge", description="This is a dummy fridge")
        test_utils.connect_fridge_user()
        test_utils.create_login_token(timezone.now() + timezone.timedelta(hours=1))
        test_utils.create_api_token(timezone.now() + timezone.timedelta(hours=1))
        self.user = Users.objects.filter(username="dummy_name").values_list("user_id").first()[0]
        self.fridge = Fridges.objects.filter(name="Dummy Fridge").values_list("fridge_id").first()[0]

    @mock.patch("Fridgify_Backend.utils.fridge_content_handler.check_item_exists")
    @mock.patch("Fridgify_Backend.utils.fridge_content_handler.get_fridge")
    def test_fridgeAddItem_ValidDataItemNotExisting_Added(self, mock_get_fridge, mock_check_exists):
        fridge = Fridges.objects.filter(name="Dummy Fridge").first()
        mock_get_fridge.return_value = fridge
        mock_check_exists.return_value = None
        request = {"name": "Item 1", "description": "This is a item",
                   "buy_date": "2019-10-17", "expiration_date": "2019-11-23",
                   "amount": 9, "unit": "kg", "store": "Rewe"}
        result = fridge_content_handler.fridge_add_item(self.fridge, self.user, request)
        self.assertEqual(result, 1)
        self.assertEqual(len(FridgeContent.objects.filter(item__name="Item 1")), 1)
        self.assertEqual(len(Items.objects.filter(name="Item 1")), 1)

    @mock.patch("Fridgify_Backend.utils.fridge_content_handler.check_item_exists")
    @mock.patch("Fridgify_Backend.utils.fridge_content_handler.get_fridge")
    def test_fridgeAddItem_ValidDataItemExisting_Added(self, mock_get_fridge, mock_check_exists):
        mock_get_fridge.return_value = Fridges.objects.filter(name="Dummy Fridge").first()
        mock_check_exists.return_value = test_utils.create_items("")
        request = {"name": "Item A", "description": "Description",
                   "buy_date": "2019-01-01", "expiration_date": "2019-01-01",
                   "amount": 1, "unit": "kg", "store": "Rewe"}
        result = fridge_content_handler.fridge_add_item(self.fridge, self.user, request)
        self.assertEqual(result, 1)
        self.assertEqual(len(FridgeContent.objects.filter(item__name="Item A")), 1)
        self.assertEqual(len(Items.objects.filter(name="Item A")), 1)

    @mock.patch("Fridgify_Backend.utils.fridge_content_handler.check_item_exists")
    @mock.patch("Fridgify_Backend.utils.fridge_content_handler.get_fridge")
    def test_fridgeAddItem_ItemError_minus1(self, mock_get_fridge, mock_check_exists):
        mock_get_fridge.return_value = Fridges.objects.filter(name="Dummy Fridge").first()
        mock_check_exists.return_value = -1
        request = {"name": "Item A", "description": "Description",
                   "buy_date": "2019-01-01", "expiration_date": "2019-01-01",
                   "amount": 1, "unit": "kg", "store": "Rewe"}
        result = fridge_content_handler.fridge_add_item(self.fridge, self.user, request)
        self.assertEqual(result, -1)

    @mock.patch("Fridgify_Backend.utils.fridge_content_handler.check_item_exists")
    @mock.patch("Fridgify_Backend.utils.fridge_content_handler.get_fridge")
    def test_fridgeAddItem_fridgeNotExisting_0(self, mock_get_fridge, mock_check_exists):
        mock_get_fridge.return_value = Fridges.objects.filter(name="Not Fridge").first()
        mock_check_exists.return_value = -1
        request = {"name": "Item A", "description": "Description",
                   "buy_date": "2019-01-01", "expiration_date": "2019-01-01",
                   "amount": 1, "unit": "kg", "store": "Rewe"}
        result = fridge_content_handler.fridge_add_item(2, 1, request)
        self.assertEqual(result, 0)

    def test_checkItemExists_ItemExists_Item(self):
        test_utils.create_items("Item A")
        result = fridge_content_handler.check_item_exists("Item A", "Rewe")
        self.assertEqual(result.name, "Item A")

    def test_checkItemExists_ItemNotExisting_None(self):
        result = fridge_content_handler.check_item_exists("Item A", "Rewe")
        self.assertIsNone(result)

    def test_fridgeGetItem_ValidFridgeUserSingle_SingleContent(self):
        test_utils.create_items("Item A")
        item_id1 = test_utils.get_item("Item A").values("item_id").first()["item_id"]
        test_utils.create_fridge_content(item_id1, self.fridge)

        result = fridge_content_handler.fridge_get_item(self.fridge, self.user)
        self.assertIsNotNone(result)
        self.assertEqual(list(result)[0]["item__name"], "Item A")

    def test_fridgeGetItem_ValidFridgeUserMulti_MultiContent(self):
        test_utils.create_items("Item A")
        test_utils.create_items("Item B")
        item_id1 = test_utils.get_item("Item A").values("item_id").first()["item_id"]
        item_id2 = test_utils.get_item("Item B").values("item_id").first()["item_id"]
        test_utils.create_fridge_content(item_id1, self.fridge)
        test_utils.create_fridge_content(item_id2, self.fridge)

        result = fridge_content_handler.fridge_get_item(self.fridge, self.user)
        self.assertIsNotNone(result)
        result_l = list(result)
        self.assertEqual(len(result_l), 2)
        self.assertEqual(result_l[0]["item__name"], "Item A")
        self.assertEqual(result_l[1]["item__name"], "Item B")

    def test_fridgeGetItem_NoContentUserNotAuth4Fridge_0(self):
        result = fridge_content_handler.fridge_get_item(self.fridge, 1000)
        self.assertIsNotNone(result)
        self.assertEqual(result, 0)

    def test_fridgeGetItem_FridgeNotExisting_None(self):
        result = fridge_content_handler.fridge_get_item(1000, self.user)
        self.assertIsNone(result)

    def test_removeItem_ExistingFridgeItem_Removed(self):
        test_utils.create_items("Item A")
        item_id = test_utils.get_item("Item A").values()[0]["item_id"]
        fridge_id = test_utils.get_fridge("Dummy Fridge").values()[0]["fridge_id"]
        test_utils.create_fridge_content(item_id, fridge_id)
        res = fridge_content_handler.remove_item(fridge_id, item_id)
        self.assertEqual(res, 1)
        obj = FridgeContent.objects.filter(item_id=item_id, fridge_id=fridge_id)
        self.assertEqual(len(obj), 0)

    def test_removeItem_NoExistingItem_Removed(self):
        test_utils.create_items("Item A")
        item_id = test_utils.get_item("Item A").values()[0]["item_id"]
        fridge_id = test_utils.get_fridge("Dummy Fridge").values()[0]["fridge_id"]
        test_utils.create_fridge_content(item_id, fridge_id)
        res = fridge_content_handler.remove_item(1000, 1000)
        self.assertEqual(res, 0)
        obj = FridgeContent.objects.filter(item_id=item_id, fridge_id=fridge_id)
        self.assertEqual(len(obj), 1)
