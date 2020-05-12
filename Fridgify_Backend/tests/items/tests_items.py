from django.utils import timezone
import json
from rest_framework import status
from unittest import mock
from django.test import TestCase, RequestFactory

from Fridgify_Backend.views.items import items
from Fridgify_Backend.tests import test_utils
from Fridgify_Backend.models import Items


class ItemsApiTestCasesGetAllItems(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        test_utils.setup()
        test_utils.create_dummyuser()
        test_utils.create_items("Item A")
        test_utils.create_items("Item B")
        test_utils.create_api_token(timezone.now() + timezone.timedelta(hours=1))

    def test_items_view_ValidTokenAndRequest_200(self):
        request = self.factory.get("/items/")
        request.META["HTTP_AUTHORIZATION"] = "APIToken"

        response = items.items_view(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
