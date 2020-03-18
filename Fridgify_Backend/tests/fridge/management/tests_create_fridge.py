from django.test import TestCase, RequestFactory
from django.utils import timezone

from rest_framework import status
from Fridgify_Backend.views.fridge.management import create_fridge
from Fridgify_Backend.tests import test_utils

import json


class ManagementTestCasesCreateFridge(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        test_utils.setup()
        user = test_utils.create_dummyuser(username="User")
        test_utils.create_login_token(timezone.now() + timezone.timedelta(days=1), username=user.username)
        test_utils.create_api_token(timezone.now() + timezone.timedelta(days=1), t="API Token", username=user.username)
        # fridge = test_utils.create_dummyfridge()
        # test_utils.connect_fridge_user(user.username, fridge.name)

    def test_create_fridge_body_validation(self):
        request = self.factory.post("/fridge/management/create/", {
            "name": "Fridge A",
            "description": "Fridge Test"
        }, content_type="application/json")
        request.META["HTTP_AUTHORIZATION"] = "API Token"

        response = create_fridge.create_fridge_view(request)

        content = json.loads(response.render().content)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(content["name"], "Fridge A")
        self.assertEqual(content["description"], "Fridge Test")

    def test_create_fridge_not_authorized_403(self):
        request = self.factory.post("/fridge/management/create/")

        response = create_fridge.create_fridge_view(request)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_fridge_already_exists(self):
        request = self.factory.post("/fridge/management/create/", {
            "name": "Fridge A",
            "description": "Fridge Test"
        }, content_type="application/json")
        fridge = test_utils.create_dummyfridge("Fridge A")
        test_utils.connect_fridge_user("User", fridge.name)

        request.META["HTTP_AUTHORIZATION"] = "API Token"

        response = create_fridge.create_fridge_view(request)
        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)
