from django.utils import timezone
import json
from rest_framework import status
from unittest import mock
from django.test import TestCase, RequestFactory

from fridgify_backend.views.fridge.content import fridge_content
from fridgify_backend.tests import test_utils
from fridgify_backend.models import Items


class ContentApiTestCasesFridgeContent(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        test_utils.setup()
        test_utils.create_dummyuser()
        test_utils.create_dummyuser("us2", "user", "name", "user@a.a")
        test_utils.create_dummyfridge()
        test_utils.connect_fridge_user()
        test_utils.create_items("Item A")
        test_utils.create_items("Item B")
        test_utils.create_login_token(timezone.now() + timezone.timedelta(hours=1))
        test_utils.create_api_token(timezone.now() + timezone.timedelta(hours=1))
        test_utils.create_api_token(timezone.now() + timezone.timedelta(hours=1), username="us2", t="APIToken2")

    def test_addFridgeContent_ValidTokenAndRequest_201(self):
        request = self.factory.post("/fridge/1", {"name": "Item 1", "description": "This is a item",
                                                  "buy_date": "2019-10-17", "expiration_date": "2019-11-23",
                                                  "count": 1, "amount": 9, "unit": "kg", "store": "Rewe"},
                                    content_type="application/json")
        request.META["HTTP_AUTHORIZATION"] = "APIToken"
        response = fridge_content.fridge_content_view(request, 1)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_addFridgeContent_NoTokenAndValidRequest_401(self):
        request = self.factory.post("/fridge/1", {"name": "Item 1", "description": "This is a item",
                                                  "buy_date": "2019-10-17", "expiration_date": "2019-11-23",
                                                  "amount": 9, "unit": "kg", "store": "Rewe"},
                                    content_type="application/json")
        response = fridge_content.fridge_content_view(request, 1)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_addFridgeContent_InvalidTokenAndRequest_403(self):
        request = self.factory.post("fridge/1", {}, content_type="application/json")
        request.META["HTTP_AUTHORIZATION"] = "NotAFuckingToken"
        response = fridge_content.fridge_content_view(request, 1)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_addFridgeContent_ValidTokenInvalidBody_400(self):
        request = self.factory.post("fridge/1", {}, content_type="application/json")
        request.META["HTTP_AUTHORIZATION"] = "APIToken"
        response = fridge_content.fridge_content_view(request, 1)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_addFridgeContent_ValidTokenMissingAttributes_400(self):
        request = self.factory.post("fridge/1", {"name":"Name"}, content_type="application/json")
        request.META["HTTP_AUTHORIZATION"] = "APIToken"
        response = fridge_content.fridge_content_view(request, 1)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_addFridgeContent_NotAuthorized_401(self):
        request = self.factory.post("/fridge/1", {"name": "Item A", "description": "This is a item",
                                                  "buy_date": "2019-10-17", "expiration_date": "2019-11-23",
                                                  "amount": 9, "unit": "kg", "store": "Rewe"},
                                    content_type="application/json")
        request.META["HTTP_AUTHORIZATION"] = "APIToken2"
        response = fridge_content.fridge_content_view(request, 1)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_getFridgeContent_ValidFridgeAndTokenWithContent_200Content(self):
        fridge_id = test_utils.get_fridge("Dummy Fridge").values("fridge_id").first()["fridge_id"]
        item_id = test_utils.get_item("Item A").values("item_id").first()["item_id"]
        test_utils.create_fridge_content(item_id, fridge_id)
        item = test_utils.get_fridge_items(fridge_id).values("item__name", "expiration_date", "amount", "unit")
        request = self.factory.get("/fridge/1")
        request.META["HTTP_AUTHORIZATION"] = "APIToken"

        res = fridge_content.fridge_content_view(request, fridge_id)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        body = json.loads(res.render().content.decode("utf-8"))
        self.assertEqual(body[0]["name"], "Item A")

    def test_getFridgeContent_ValidFridgeAndTokenWithMultiContent_200MultiContent(self):
        fridge_id = test_utils.get_fridge("Dummy Fridge").values("fridge_id").first()["fridge_id"]
        item_id1 = test_utils.get_item("Item A").values("item_id").first()["item_id"]
        item_id2 = test_utils.get_item("Item B").values("item_id").first()["item_id"]
        test_utils.create_fridge_content(item_id1, fridge_id)
        test_utils.create_fridge_content(item_id2, fridge_id)

        request = self.factory.get(f"/fridge/{fridge_id}")
        request.META["HTTP_AUTHORIZATION"] = "APIToken"

        res = fridge_content.fridge_content_view(request, fridge_id)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        body = json.loads(res.render().content.decode("utf-8"))
        self.assertEqual(body[0]["name"], "Item A")
        self.assertEqual(body[1]["name"], "Item B")

    def test_getFridgeContent_InvalidToken_403(self):
        request = self.factory.get("/fridge/1")
        request.META["HTTP_AUTHORIZATION"] = "NotAValidToken"

        res = fridge_content.fridge_content_view(request, 1)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_getFridgeContent_NoAccess(self):
        fridge_id = test_utils.get_fridge("Dummy Fridge").values("fridge_id").first()["fridge_id"]
        request = self.factory.get("/fridge/1")
        request.META["HTTP_AUTHORIZATION"] = "APIToken2"

        res = fridge_content.fridge_content_view(request, fridge_id)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_getFridgeContent_NoToken_401(self):
        request = self.factory.get("/fridge/1")

        res = fridge_content.fridge_content_view(request, 1)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_getFridgeContent_UserNotAuthForFridge_401(self):
        fridge_id = test_utils.get_fridge("Dummy Fridge").values("fridge_id").first()["fridge_id"]
        request = self.factory.get("/fridge/1")
        request.META["HTTP_AUTHORIZATION"] = "APIToken2"

        res = fridge_content.fridge_content_view(request, fridge_id)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
