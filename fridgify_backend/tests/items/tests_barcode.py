from django.utils import timezone
import json
from rest_framework import status
from unittest import mock
from django.test import TestCase, RequestFactory

from fridgify_backend.views.items import barcode
from fridgify_backend.tests import test_utils
from fridgify_backend.models import Items, ItemsSerializer


class ItemsApiTestCasesGetWithBarcode(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        test_utils.setup()
        test_utils.create_dummyuser()
        test_utils.create_items("Item A")
        test_utils.create_items("Item B")
        test_utils.create_api_token(timezone.now() + timezone.timedelta(hours=1))

    def test_barcode_view_ItemExists_200(self):
        barcode_string = ItemsSerializer(test_utils.create_items("Item C")).data["barcode"]
        request = self.factory.get(f"/items/barcode/{barcode_string}/")
        request.META["HTTP_AUTHORIZATION"] = "APIToken"

        response = barcode.barcode_view(request, barcode_string)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_barcode_view_ItemDoesntExist_404(self):
        request = self.factory.get(f"/items/barcode/999/")
        request.META["HTTP_AUTHORIZATION"] = "APIToken"

        response = barcode.barcode_view(request, 999)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_barcode_view_ItemIdIsMissing(self):
        request = self.factory.get(f"/items/barcode/")
        request.META["HTTP_AUTHORIZATION"] = "APIToken"

        response = barcode.barcode_view(request, None)
        self.assertEqual(response.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)
