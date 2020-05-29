from django.utils import timezone
import json
from rest_framework import status
from unittest import mock
from django.test import TestCase, RequestFactory

from fridgify_backend.views.items import id
from fridgify_backend.tests import test_utils
from fridgify_backend.models import Items, ItemsSerializer


class ItemsApiTestCasesGetWithId(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        test_utils.setup()
        test_utils.create_dummyuser()
        test_utils.create_items("Item A")
        test_utils.create_items("Item B")
        test_utils.create_api_token(timezone.now() + timezone.timedelta(hours=1))

    def test_id_view_ItemExists_200(self):
        item_id = ItemsSerializer(test_utils.create_items("Item C")).data["item_id"]
        request = self.factory.get(f"/items/id/{item_id}/")
        request.META["HTTP_AUTHORIZATION"] = "APIToken"

        response = id.id_view(request, item_id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_id_view_ItemDoesntExist_404(self):
        request = self.factory.get(f"/items/id/999/")
        request.META["HTTP_AUTHORIZATION"] = "APIToken"

        response = id.id_view(request, 999)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_id_view_ItemIdIsMissing(self):
        request = self.factory.get(f"/items/id/")
        request.META["HTTP_AUTHORIZATION"] = "APIToken"

        response = id.id_view(request, None)
        self.assertEqual(response.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)
