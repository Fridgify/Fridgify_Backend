"""Test file for Items"""

from django.utils import timezone
from django.test import TestCase, RequestFactory
from rest_framework import status

from fridgify_backend.views.items import items
from fridgify_backend.tests import test_utils


class ItemsApiTestCasesGetAllItems(TestCase):
    """TestCase for items view"""
    def setUp(self):
        """Setup for test case"""
        self.factory = RequestFactory()
        test_utils.setup()
        test_utils.create_dummyuser()
        test_utils.create_items("Item A")
        test_utils.create_items("Item B")
        test_utils.create_api_token(timezone.now() + timezone.timedelta(hours=1))

    def test_items_view_valid_token_and_request_exp_200(self):
        """Get items successfully. Expecting 200 response"""
        request = self.factory.get("/items/")
        request.META["HTTP_AUTHORIZATION"] = "APIToken"

        response = items.items_view(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
