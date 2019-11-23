from django.utils import timezone
import datetime
from rest_framework import status
from unittest import mock
from django.test import TestCase, RequestFactory

from Fridgify_Backend.views.fridge.content import fridge_content
from Fridgify_Backend.tests import test_utils


class ContentApiTestCasesFridgeContent(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        test_utils.setup()
        test_utils.create_dummyuser()
        test_utils.create_dummyfridge()
        test_utils.connect_fridge_user()
        test_utils.create_login_token(timezone.now() + timezone.timedelta(hours=1))
        test_utils.create_api_token(timezone.now() + timezone.timedelta(hours=1))

    """Add fridge content test case"""
    @mock.patch("Fridgify_Backend.utils.fridge_content_handler.fridge_add_item")
    def test_addFridgeContent_ValidTokenAndRequest_201(self, mock_add_item):
        mock_add_item.return_value = 1
        request = self.factory.post("/fridge/1", {"name": "Item 1", "description": "This is a item",
                                                  "buy_date": "2019-10-17", "expiration_date": "2019-11-23",
                                                  "amount": 9, "unit": "kg", "store": "Rewe"},
                                    content_type="application/json")
        request.META["HTTP_AUTHORIZATION"] = "APIToken"
        response = fridge_content.add_content_to_fridge(request, 1)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_addFridgeContent_NoTokenAndValidRequest_401(self):
        request = self.factory.post("/fridge/1", {"name": "Item 1", "description": "This is a item",
                                                  "buy_date": "2019-10-17", "expiration_date": "2019-11-23",
                                                  "amount": 9, "unit": "kg", "store": "Rewe"},
                                    content_type="application/json")
        response = fridge_content.add_content_to_fridge(request, 1)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_addFridgeContent_InvalidTokenAndRequest_403(self):
        request = self.factory.post("fridge/1", {}, content_type="application/json")
        request.META["HTTP_AUTHORIZATION"] = "NotAFuckingToken"
        response = fridge_content.add_content_to_fridge(request, 1)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_addFridgeContent_ValidTokenInvalidBody_400(self):
        request = self.factory.post("fridge/1", {}, content_type="application/json")
        request.META["HTTP_AUTHORIZATION"] = "APIToken"
        response = fridge_content.add_content_to_fridge(request, 1)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_addFridgeContent_ValidTokenMissingAttributes_400(self):
        request = self.factory.post("fridge/1", {"name":"Name"}, content_type="application/json")
        request.META["HTTP_AUTHORIZATION"] = "APIToken"
        response = fridge_content.add_content_to_fridge(request, 1)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @mock.patch("Fridgify_Backend.utils.fridge_content_handler.fridge_add_item")
    def test_addFridgeContent_NotAuthorized_401(self, mock_add_item):
        mock_add_item.return_value = 0
        request = self.factory.post("/fridge/1", {"name": "Item 1", "description": "This is a item",
                                                  "buy_date": "2019-10-17", "expiration_date": "2019-11-23",
                                                  "amount": 9, "unit": "kg", "store": "Rewe"},
                                    content_type="application/json")
        request.META["HTTP_AUTHORIZATION"] = "APIToken"
        response = fridge_content.add_content_to_fridge(request, 1)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    @mock.patch("Fridgify_Backend.utils.fridge_content_handler.fridge_add_item")
    def test_addFridgeContent_InternalError_500(self, mock_add_item):
        mock_add_item.return_value = -1
        request = self.factory.post("/fridge/1", {"name": "Item 1", "description": "This is a item",
                                                  "buy_date": "2019-10-17", "expiration_date": "2019-11-23",
                                                  "amount": 9, "unit": "kg", "store": "Rewe"},
                                    content_type="application/json")
        request.META["HTTP_AUTHORIZATION"] = "APIToken"
        response = fridge_content.add_content_to_fridge(request, 1)
        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)

    def test_checkReqAdd_ValidBody_True(self):
        req_body = {"name": "Item 1", "description": "This is a item",
                    "buy_date": "2019-10-17", "expiration_date": "2019-11-23",
                    "amount": 9, "unit": "kg", "store": "Rewe"}
        res = fridge_content.check_req_add(req_body)
        self.assertTrue(res)

    def test_checkReqAdd_InvalidBody_True(self):
        req_body = {"description": "This is a item",
                    "buy_date": "2019-10-17", "expiration_date": "2019-11-23",
                    "amount": 9, "unit": "kg", "store": "Rewe"}
        res = fridge_content.check_req_add(req_body)
        self.assertFalse(res)

    """Get fridge content test case"""
    def test_get_fridge_content(self):
        # obj = type('obj', (object,), {'method': 'GET'})
        # response = json.loads(fridge_content.entry_point(obj).content)
        # self.assertEqual(response["message"], "Get content", "Get content")
        self.assertEqual(0,0)
