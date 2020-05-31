"""Test file for Create Fridge"""
# pylint: disable=no-member

import json

from django.test import TestCase, RequestFactory
from django.utils import timezone
from rest_framework import status

from fridgify_backend.views.fridge.management import create_fridge
from fridgify_backend.tests import test_utils


class ManagementTestCasesCreateFridge(TestCase):
    """Test Case for create fridge view"""
    def setUp(self):
        """Setup for test case"""
        self.factory = RequestFactory()
        test_utils.setup()
        user = test_utils.create_dummyuser(username="User")
        test_utils.create_login_token(
            timezone.now() + timezone.timedelta(days=1),
            username=user.username
        )
        test_utils.create_api_token(
            timezone.now() + timezone.timedelta(days=1),
            tok="API Token",
            username=user.username
        )

    def test_create_fridge_body_validation(self):
        """Create a fridge. Check for valid body. Expecting 201 response"""
        request = self.factory.post(
            "/fridge/management/create/",
            {"name": "Fridge A", "description": "Fridge Test"},
            content_type="application/json"
        )
        request.META["HTTP_AUTHORIZATION"] = "API Token"

        response = create_fridge.create_fridge_view(request)

        content = json.loads(response.render().content)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(content["name"], "Fridge A")
        self.assertEqual(content["description"], "Fridge Test")

    def test_create_fridge_not_authorized_403(self):
        """Create a fridge with missing token. Expecting 403 response"""
        request = self.factory.post("/fridge/management/create/")

        response = create_fridge.create_fridge_view(request)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_fridge_already_exists(self):
        """Create a fridge, which already exists. Expecting 409 response"""
        request = self.factory.post(
            "/fridge/management/create/",
            {"name": "Fridge A", "description": "Fridge Test"},
            content_type="application/json"
        )
        fridge = test_utils.create_dummyfridge("Fridge A")
        test_utils.connect_fridge_user("User", fridge.name)

        request.META["HTTP_AUTHORIZATION"] = "API Token"

        response = create_fridge.create_fridge_view(request)
        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)
