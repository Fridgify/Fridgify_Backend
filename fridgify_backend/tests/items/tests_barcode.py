"""Test file for Item Barcode"""

from django.utils import timezone
from django.test import TestCase, RequestFactory
from rest_framework import status

from fridgify_backend.views.items import barcode
from fridgify_backend.tests import test_utils
from fridgify_backend.models import ItemsSerializer


class ItemsApiTestCasesGetWithBarcode(TestCase):
    """TestCase for item with barcode"""
    def setUp(self):
        """Setup for test case"""
        self.factory = RequestFactory()
        test_utils.setup()
        test_utils.create_dummyuser()
        test_utils.create_items("Item A")
        test_utils.create_items("Item B")
        test_utils.create_api_token(timezone.now() + timezone.timedelta(hours=1))

    def test_barcode_view_exp_item_exists_200(self):
        """Get item w/ barcode. Expecting 200 response"""
        barcode_string = ItemsSerializer(test_utils.create_items("Item C")).data["barcode"]
        request = self.factory.get(f"/items/barcode/{barcode_string}/")
        request.META["HTTP_AUTHORIZATION"] = "APIToken"

        response = barcode.barcode_view(request, barcode_string)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_barcode_view_item_doesnt_exist_404(self):
        """Get item w/ barcode. Item does not exist. Expecting 404 response"""
        request = self.factory.get("/items/barcode/999/")
        request.META["HTTP_AUTHORIZATION"] = "APIToken"

        response = barcode.barcode_view(request, 999)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_barcode_view_item_id_is_missing(self):
        """Get item w/ barcode. Item ID is missing. Expecting 422 response"""
        request = self.factory.get("/items/barcode/")
        request.META["HTTP_AUTHORIZATION"] = "APIToken"

        response = barcode.barcode_view(request, None)
        self.assertEqual(response.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)
