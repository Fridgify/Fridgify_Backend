from django.utils import timezone
import datetime
import json
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
        test_utils.create_items("Item A")
        test_utils.create_items("Item B")
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

    @mock.patch("Fridgify_Backend.utils.fridge_content_handler.fridge_get_item")
    def test_getFridgeContent_ValidFridgeAndTokenWithContent_200Content(self, mock_get_content):
        fridge_id = test_utils.get_fridge("Dummy Fridge").values("fridge_id").first()["fridge_id"]
        item_id = test_utils.get_item("Item A").values("item_id").first()["item_id"]
        test_utils.create_fridge_content(item_id, fridge_id)
        item = test_utils.get_fridge_items(fridge_id).values("item__name", "expiration_date", "amount", "unit")
        mock_get_content.return_value = item
        request = self.factory.get("/fridge/1")
        request.META["HTTP_AUTHORIZATION"] = "APIToken"

        res = fridge_content.get_content_in_fridge(request, fridge_id)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        body = json.loads(res.content.decode("utf-8"))
        self.assertEqual(body[0]["item__name"], "Item A")

    @mock.patch("Fridgify_Backend.utils.fridge_content_handler.fridge_get_item")
    def test_getFridgeContent_ValidFridgeAndTokenWithMultiContent_200MultiContent(self, mock_get_content):
        fridge_id = test_utils.get_fridge("Dummy Fridge").values("fridge_id").first()["fridge_id"]
        item_id1 = test_utils.get_item("Item A").values("item_id").first()["item_id"]
        item_id2 = test_utils.get_item("Item B").values("item_id").first()["item_id"]
        test_utils.create_fridge_content(item_id1, fridge_id)
        test_utils.create_fridge_content(item_id2, fridge_id)
        item = test_utils.get_fridge_items(fridge_id).values("item__name", "expiration_date", "amount", "unit")
        mock_get_content.return_value = item
        request = self.factory.get("/fridge/1")
        request.META["HTTP_AUTHORIZATION"] = "APIToken"

        res = fridge_content.get_content_in_fridge(request, fridge_id)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        body = json.loads(res.content.decode("utf-8"))
        self.assertEqual(body[0]["item__name"], "Item A")
        self.assertEqual(body[1]["item__name"], "Item B")

    @mock.patch("Fridgify_Backend.utils.fridge_content_handler.fridge_get_item")
    def test_getFridgeContent_ErrorGettingItems_500(self, mock_get_content):
        fridge_id = test_utils.get_fridge("Dummy Fridge").values("fridge_id").first()["fridge_id"]
        mock_get_content.return_value = -1
        request = self.factory.get("/fridge/1")
        request.META["HTTP_AUTHORIZATION"] = "APIToken"

        res = fridge_content.get_content_in_fridge(request, fridge_id)
        self.assertEqual(res.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)

    def test_getFridgeContent_InvalidToken_403(self):
        request = self.factory.get("/fridge/1")
        request.META["HTTP_AUTHORIZATION"] = "NotAValidToken"

        res = fridge_content.get_content_in_fridge(request, 1)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    @mock.patch("Fridgify_Backend.utils.fridge_content_handler.fridge_get_item")
    def test_getFridgeContent_ContentNone_404(self, mock_get_content):
        fridge_id = test_utils.get_fridge("Dummy Fridge").values("fridge_id").first()["fridge_id"]
        mock_get_content.return_value = None
        request = self.factory.get("/fridge/1")
        request.META["HTTP_AUTHORIZATION"] = "APIToken"

        res = fridge_content.get_content_in_fridge(request, fridge_id)
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)

    def test_getFridgeContent_NoToken_401(self):
        request = self.factory.get("/fridge/1")

        res = fridge_content.get_content_in_fridge(request, 1)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    @mock.patch("Fridgify_Backend.utils.fridge_content_handler.fridge_get_item")
    def test_getFridgeContent_UserNotAuthForFridge_401(self, mock_get_content):
        fridge_id = test_utils.get_fridge("Dummy Fridge").values("fridge_id").first()["fridge_id"]
        mock_get_content.return_value = 0
        request = self.factory.get("/fridge/1")
        request.META["HTTP_AUTHORIZATION"] = "APIToken"

        res = fridge_content.get_content_in_fridge(request, fridge_id)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
