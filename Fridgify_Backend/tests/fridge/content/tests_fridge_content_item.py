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
        test_utils.create_items("Item B")
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

    def test_removeContentInFridge_ValidRequest_200(self):
        request = self.factory.delete("/fridge/content/1/1", content_type="application/json")
        request.META["HTTP_AUTHORIZATION"] = "APIToken"
        res = fridge_content_item.fridge_content_item_view(request,
                                                           test_utils.get_fridge("Dummy Fridge").values("fridge_id").first()["fridge_id"],
                                                           test_utils.get_item("Item A").values("item_id").first()["item_id"])
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_removeContentInFridge_MissingAuthorization_401(self):
        request = self.factory.delete("/fridge/content/1/1")
        res = fridge_content_item.fridge_content_item_view(request,
                                                           test_utils.get_fridge("Dummy Fridge").values(
                                                               "fridge_id").first()["fridge_id"],
                                                           test_utils.get_item("Item A").values("item_id").first()["item_id"])
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_removeContentInFridge_NoItem_200(self):
        request = self.factory.delete("/fridge/content/1/1")
        request.META["HTTP_AUTHORIZATION"] = "APIToken"
        test_utils.create_fridge_content(
            test_utils.get_item("Item B").first().item_id,
            test_utils.get_fridge("Dummy Fridge").first().fridge_id,
        )
        res = fridge_content_item.fridge_content_item_view(request,
                                                           test_utils.get_fridge("Dummy Fridge").values(
                                                               "fridge_id").first()["fridge_id"],
                                                           test_utils.get_item("Item B").values("item_id").first()["item_id"])
        self.assertEqual(res.status_code, status.HTTP_200_OK)
