"""Test file for FridgeContent Item"""
# pylint: disable=no-member

from django.test import TestCase, RequestFactory
from django.utils import timezone
from rest_framework import status

from fridgify_backend.views.fridge.content import fridge_content_item
from fridgify_backend.tests import test_utils


class ContentApiTestCasesFridgeContentItem(TestCase):
    """TestCase for fridge content item view"""
    def setUp(self):
        """Setup for test case"""
        self.factory = RequestFactory()
        test_utils.setup()
        test_utils.create_dummyuser()
        test_utils.create_dummyfridge()
        test_utils.connect_fridge_user()
        test_utils.create_login_token(
            timezone.now() + timezone.timedelta(days=14)
        )
        test_utils.create_api_token(
            timezone.now() + timezone.timedelta(days=14)
        )
        test_utils.create_items("Item A")
        test_utils.create_items("Item B")
        test_utils.create_fridge_content(
            test_utils.get_item("Item A").values()[0]["item_id"],
            test_utils.get_fridge("Dummy Fridge").values()[0]["fridge_id"]
        )

    def test_remove_content_valid_request_exp_200(self):
        """Remove content with valid body. Expecting 200 response"""
        request = self.factory.delete(
            "/fridge/content/1/1",
            content_type="application/json"
        )
        request.META["HTTP_AUTHORIZATION"] = "APIToken"
        res = fridge_content_item.fridge_content_item_view(
            request,
            test_utils.get_fridge("Dummy Fridge").values("fridge_id").first()["fridge_id"],
            test_utils.get_item("Item A").values("item_id").first()["item_id"])
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_remove_content_missing_authorization_exp_401(self):
        """Remove content with missing authorization. Expecting 401 response"""
        request = self.factory.delete("/fridge/content/1/1")
        res = fridge_content_item.fridge_content_item_view(
            request,
            test_utils.get_fridge(
                "Dummy Fridge"
            ).values("fridge_id").first()["fridge_id"],
            test_utils.get_item("Item A").values("item_id").first()["item_id"])
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
