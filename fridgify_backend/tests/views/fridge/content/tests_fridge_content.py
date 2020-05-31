"""Test file for FridgeContent"""
# pylint: disable=no-member

import json

from django.utils import timezone
from django.test import TestCase, RequestFactory
from rest_framework import status

from fridgify_backend.views.fridge.content import fridge_content
from fridgify_backend.tests import test_utils


class ContentApiTestCasesFridgeContent(TestCase):
    """TestCase for fridge content view"""
    def setUp(self):
        """Setup for test case"""
        self.factory = RequestFactory()
        test_utils.setup()
        test_utils.create_dummyuser()
        test_utils.create_dummyuser("us2", "user", "name", "user@a.a")
        test_utils.create_dummyfridge()
        test_utils.connect_fridge_user()
        test_utils.create_items("Item A")
        test_utils.create_items("Item B")
        test_utils.create_login_token(
            timezone.now() + timezone.timedelta(hours=1)
        )
        test_utils.create_api_token(
            timezone.now() + timezone.timedelta(hours=1)
        )
        test_utils.create_api_token(
            timezone.now() + timezone.timedelta(hours=1),
            username="us2",
            tok="APIToken2"
        )

    def test_add_fridge_content_valid_token_and_request_exp_201(self):
        """Add content with valid token & body. Expecting 201 response"""
        request = self.factory.post(
            "/fridge/1",
            {
                "name": "Item 1",
                "description": "This is a item",
                "buy_date": "2019-10-17",
                "expiration_date": "2019-11-23",
                "count": 1,
                "amount": 9,
                "unit": "kg",
                "store": "Rewe"
            },
            content_type="application/json"
        )
        request.META["HTTP_AUTHORIZATION"] = "APIToken"
        response = fridge_content.fridge_content_view(request, 1)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_add_fridge_content_no_token_and_valid_request_exp_401(self):
        """Add content with missing token. Expecting 401 response"""
        request = self.factory.post(
            "/fridge/1",
            {
                "name": "Item 1",
                "description": "This is a item",
                "buy_date": "2019-10-17",
                "expiration_date": "2019-11-23",
                "amount": 9,
                "unit": "kg",
                "store": "Rewe"
            },
            content_type="application/json"
        )
        response = fridge_content.fridge_content_view(request, 1)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_add_fridge_content_invalid_token_and_request_exp_403(self):
        """Add content with invalid token. Expecting 403 response"""
        request = self.factory.post(
            "fridge/1",
            {},
            content_type="application/json"
        )
        request.META["HTTP_AUTHORIZATION"] = "NotAFuckingToken"
        response = fridge_content.fridge_content_view(request, 1)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_add_fridge_content_valid_token_invalid_body_exp_400(self):
        """Add content with valid token/invalid body. Expecting 400 response"""
        request = self.factory.post("fridge/1", {}, content_type="application/json")
        request.META["HTTP_AUTHORIZATION"] = "APIToken"
        response = fridge_content.fridge_content_view(request, 1)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_add_fridge_content_valid_token_missing_attributes_exp_400(self):
        """Add content with valid token/incomplete body. Expecting 400 response"""
        request = self.factory.post(
            "fridge/1",
            {"name": "Name"},
            content_type="application/json"
        )
        request.META["HTTP_AUTHORIZATION"] = "APIToken"
        response = fridge_content.fridge_content_view(request, 1)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_add_fridge_content_not_authorized_exp_401(self):
        """Add content with no token. Expecting 401 response"""
        request = self.factory.post(
            "/fridge/1",
            {
                "name": "Item A",
                "description": "This is a item",
                "buy_date": "2019-10-17",
                "expiration_date": "2019-11-23",
                "amount": 9,
                "unit": "kg",
                "store": "Rewe"
            },
            content_type="application/json"
        )
        request.META["HTTP_AUTHORIZATION"] = "APIToken2"
        response = fridge_content.fridge_content_view(request, 1)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_content_valid_fridge_token_content_exp_200_content(self):
        """Get content with valid fridge, token. Expecting 200 response"""
        fridge_id = test_utils.get_fridge("Dummy Fridge").values("fridge_id").first()["fridge_id"]
        item_id = test_utils.get_item("Item A").values("item_id").first()["item_id"]
        test_utils.create_fridge_content(item_id, fridge_id)
        request = self.factory.get("/fridge/1")
        request.META["HTTP_AUTHORIZATION"] = "APIToken"

        res = fridge_content.fridge_content_view(request, fridge_id)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        body = json.loads(res.render().content.decode("utf-8"))
        self.assertEqual(body[0]["name"], "Item A")

    def test_get_content_valid_fridge_token_content_exp_200_multi_content(self):
        """Get multiple content with valid fridge, token. Expecting 200 response"""
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

    def test_get_content_invalid_token_exp_403(self):
        """Get content with invalid token. Expecting 403 response"""
        request = self.factory.get("/fridge/1")
        request.META["HTTP_AUTHORIZATION"] = "NotAValidToken"

        res = fridge_content.fridge_content_view(request, 1)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_content_exp_no_access(self):
        """Get content with no fridge access. Expecting 403 response"""
        fridge_id = test_utils.get_fridge("Dummy Fridge").values("fridge_id").first()["fridge_id"]
        request = self.factory.get("/fridge/1")
        request.META["HTTP_AUTHORIZATION"] = "APIToken2"

        res = fridge_content.fridge_content_view(request, fridge_id)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_content_no_token_exp_403(self):
        """Get content with not token. Expecting 403 response"""
        request = self.factory.get("/fridge/1")

        res = fridge_content.fridge_content_view(request, 1)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_content_user_not_authorized_for_fridge_exp_403(self):
        """Get content with unauthorized user. Expecting 403 response"""
        fridge_id = test_utils.get_fridge("Dummy Fridge").values("fridge_id").first()["fridge_id"]
        request = self.factory.get("/fridge/1")
        request.META["HTTP_AUTHORIZATION"] = "APIToken2"

        res = fridge_content.fridge_content_view(request, fridge_id)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
