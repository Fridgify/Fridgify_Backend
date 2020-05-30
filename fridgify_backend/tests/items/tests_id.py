"""Test file for Item ID"""

from django.utils import timezone
from django.test import TestCase, RequestFactory
from rest_framework import status

from fridgify_backend.views.items import items_id
from fridgify_backend.tests import test_utils
from fridgify_backend.models import ItemsSerializer


class ItemsApiTestCasesGetWithId(TestCase):
    """TestCase for item id view"""
    def setUp(self):
        """Setup for test case"""
        self.factory = RequestFactory()
        test_utils.setup()
        test_utils.create_dummyuser()
        test_utils.create_items("Item A")
        test_utils.create_items("Item B")
        test_utils.create_api_token(timezone.now() + timezone.timedelta(hours=1))

    def test_id_view_item_exists_exp_200(self):
        """Get item w/ id successfully. Expecting 200 response"""
        item_id = ItemsSerializer(test_utils.create_items("Item C")).data["item_id"]
        request = self.factory.get(f"/items/id/{item_id}/")
        request.META["HTTP_AUTHORIZATION"] = "APIToken"

        response = items_id.id_view(request, item_id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_id_view_item_doesnt_exist_exp_404(self):
        """Get item w/ id. Item does not exist. Expecting 404 response"""
        request = self.factory.get("/items/id/999/")
        request.META["HTTP_AUTHORIZATION"] = "APIToken"

        response = items_id.id_view(request, 999)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_id_view_item_id_is_missing(self):
        """Get item w/ id. ID is missing. Expecting 422 response"""
        request = self.factory.get("/items/id/")
        request.META["HTTP_AUTHORIZATION"] = "APIToken"

        response = items_id.id_view(request, None)
        self.assertEqual(response.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)
