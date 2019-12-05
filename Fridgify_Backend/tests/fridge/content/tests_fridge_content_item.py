import json
from unittest import mock
from django.test import TestCase, RequestFactory
from django.utils import timezone
from rest_framework import status
from Fridgify_Backend.views.fridge.content import fridge_content_item
from Fridgify_Backend.tests import test_utils


class ContentApiTestCasesFridgeContentItem(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        test_utils.setup()
        test_utils.create_dummyuser()
        test_utils.create_dummyfridge()
        test_utils.connect_fridge_user()
        test_utils.create_login_token(timezone.now() + timezone.timedelta(days=14))
        test_utils.create_api_token(timezone.now() + timezone.timedelta(days=14))
        test_utils.create_items("Item A")
        test_utils.create_fridge_content(test_utils.get_item("Item A").values()[0]["item_id"],
                                         test_utils.get_fridge("Dummy Fridge").values()[0]["fridge_id"])


    """Change the volume of an item"""
    def test_add_fridge_content_item(self):
        # response = json.loads(fridge_content_item.entry_point("POST").content)
        # self.assertEqual(response["message"], "Add item", "Add item")
        pass

    """Get fridge content item test case"""
    def test_get_fridge_content_item(self):
        # response = json.loads(fridge_content_item.entry_point("GET").content)
        # self.assertEqual(response["message"], "Get item", "Get item")
        pass

    @mock.patch("Fridgify_Backend.utils.fridge_content_handler.remove_item")
    def test_removeContentInFridge_ValidRequest_200(self, mock_remove_item):
        mock_remove_item.return_value = 1
        request = self.factory.post("/fridge/content/1/1", {"name": "Item A", "store": "Rewe",
                                                            "description": "This is an item", "amount": 10,
                                                            "unit": "kg", "buy_date": "2019-09-12",
                                                            "expiration_date": "2019-10-12"},
                                    content_type="application/json")
        request.META["HTTP_AUTHORIZATION"] = "APIToken"
        res = fridge_content_item.remove_content_in_fridge(request,
                                                           test_utils.get_fridge("Dummy Fridge").values("fridge_id").first(),
                                                           test_utils.get_item("Item A").values("item_id").first())
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    @mock.patch("Fridgify_Backend.utils.fridge_content_handler.remove_item")
    def test_removeContentInFridge_MissingAuthorization_401(self, mock_remove_item):
        mock_remove_item.return_value = 1
        request = self.factory.post("/fridge/content/1/1", {"name": "Item A", "store": "Rewe",
                                                            "description": "This is an item", "amount": 10,
                                                            "unit": "kg", "buy_date": "2019-09-12",
                                                            "expiration_date": "2019-10-12"},
                                    content_type="application/json")
        res = fridge_content_item.remove_content_in_fridge(request,
                                                           test_utils.get_fridge("Dummy Fridge").values(
                                                               "fridge_id").first(),
                                                           test_utils.get_item("Item A").values("item_id").first())
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    @mock.patch("Fridgify_Backend.utils.fridge_content_handler.remove_item")
    def test_removeContentInFridge_NoItem_200(self, mock_remove_item):
        mock_remove_item.return_value = 0
        request = self.factory.post("/fridge/content/1/1", {"name": "Item B", "store": "Rewe",
                                                            "description": "This is an item", "amount": 10,
                                                            "unit": "kg", "buy_date": "2019-09-12",
                                                            "expiration_date": "2019-10-12"},
                                    content_type="application/json")
        request.META["HTTP_AUTHORIZATION"] = "APIToken"
        res = fridge_content_item.remove_content_in_fridge(request,
                                                           test_utils.get_fridge("Dummy Fridge").values(
                                                               "fridge_id").first(),
                                                           test_utils.get_item("Item B").values("item_id").first())
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)

    @mock.patch("Fridgify_Backend.utils.fridge_content_handler.remove_item")
    def test_removeContentInFridge_InternalError_500(self, mock_remove_item):
        mock_remove_item.return_value = -1
        request = self.factory.post("/fridge/content/1/1", {"name": "Item A", "store": "Rewe",
                                                            "description": "This is an item", "amount": 10,
                                                            "unit": "kg", "buy_date": "2019-09-12",
                                                            "expiration_date": "2019-10-12"},
                                    content_type="application/json")
        request.META["HTTP_AUTHORIZATION"] = "APIToken"
        res = fridge_content_item.remove_content_in_fridge(request,
                                                           test_utils.get_fridge("Dummy Fridge").values(
                                                               "fridge_id").first(),
                                                           test_utils.get_item("Item A").values("item_id").first())
        self.assertEqual(res.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
