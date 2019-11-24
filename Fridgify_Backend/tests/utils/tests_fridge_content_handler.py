from django.utils import timezone
from unittest import mock
from django.test import TestCase, RequestFactory

from Fridgify_Backend.utils import fridge_content_handler
from Fridgify_Backend.models.fridges import Fridges
from Fridgify_Backend.models.fridge_content import FridgeContent
from Fridgify_Backend.models.items import Items
from Fridgify_Backend.tests import test_utils


class UtilsTestCaseFridgeContentHandler(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        test_utils.setup()
        test_utils.create_dummyuser()
        Fridges.objects.create(name="Dummy Fridge", description="This is a dummy fridge")
        test_utils.create_login_token(timezone.now() + timezone.timedelta(hours=1))
        test_utils.create_api_token(timezone.now() + timezone.timedelta(hours=1))

    @mock.patch("Fridgify_Backend.utils.fridge_content_handler.check_item_exists")
    @mock.patch("Fridgify_Backend.utils.fridge_content_handler.get_fridge")
    def test_fridgeAddItem_ValidDataItemNotExisting_Added(self, mock_get_fridge, mock_check_exists):
        Fridges.objects.create(name="Dummy Fridge", description="This is a dummy fridge")
        test_utils.connect_fridge_user()
        fridge = Fridges.objects.filter(name="Dummy Fridge").first()
        mock_get_fridge.return_value = fridge
        mock_check_exists.return_value = None
        request = {"name": "Item 1", "description": "This is a item",
                   "buy_date": "2019-10-17", "expiration_date": "2019-11-23",
                   "amount": 9, "unit": "kg", "store": "Rewe"}
        result = fridge_content_handler.fridge_add_item(1, 1, request)
        self.assertEqual(result, 1)
        self.assertEqual(len(FridgeContent.objects.filter(item__name="Item 1")), 1)
        self.assertEqual(len(Items.objects.filter(name="Item 1")), 1)

    @mock.patch("Fridgify_Backend.utils.fridge_content_handler.check_item_exists")
    @mock.patch("Fridgify_Backend.utils.fridge_content_handler.get_fridge")
    def test_fridgeAddItem_ValidDataItemExisting_Added(self, mock_get_fridge, mock_check_exists):
        Fridges.objects.create(name="Dummy Fridge", description="This is a dummy fridge")
        test_utils.connect_fridge_user()
        mock_get_fridge.return_value = Fridges.objects.filter(name="Dummy Fridge").first()
        mock_check_exists.return_value = test_utils.create_items("")
        request = {"name": "Item A", "description": "Description",
                   "buy_date": "2019-01-01", "expiration_date": "2019-01-01",
                   "amount": 1, "unit": "kg", "store": "Rewe"}
        result = fridge_content_handler.fridge_add_item(1, 1, request)
        self.assertEqual(result, 1)
        self.assertEqual(len(FridgeContent.objects.filter(item__name="Item A")), 1)
        self.assertEqual(len(Items.objects.filter(name="Item A")), 1)

    @mock.patch("Fridgify_Backend.utils.fridge_content_handler.check_item_exists")
    @mock.patch("Fridgify_Backend.utils.fridge_content_handler.get_fridge")
    def test_fridgeAddItem_ItemError_minus1(self, mock_get_fridge, mock_check_exists):
        Fridges.objects.create(name="Dummy Fridge", description="This is a dummy fridge")
        test_utils.connect_fridge_user()
        mock_get_fridge.return_value = Fridges.objects.filter(name="Dummy Fridge").first()
        mock_check_exists.return_value = -1
        request = {"name": "Item A", "description": "Description",
                   "buy_date": "2019-01-01", "expiration_date": "2019-01-01",
                   "amount": 1, "unit": "kg", "store": "Rewe"}
        result = fridge_content_handler.fridge_add_item(1, 1, request)
        self.assertEqual(result, -1)

    @mock.patch("Fridgify_Backend.utils.fridge_content_handler.check_item_exists")
    @mock.patch("Fridgify_Backend.utils.fridge_content_handler.get_fridge")
    def test_fridgeAddItem_fridgeNotExisting_0(self, mock_get_fridge, mock_check_exists):
        Fridges.objects.create(name="Dummy Fridge", description="This is a dummy fridge")
        test_utils.connect_fridge_user()
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
