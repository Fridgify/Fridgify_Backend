"""Test file for Register for Messaging"""
# pylint: disable=no-member

from django.utils import timezone
from django.test import TestCase, RequestFactory
from rest_framework import status

from fridgify_backend.models import Accesstokens
from fridgify_backend.tests import test_utils
from fridgify_backend.views.messaging import register


class TestCaseMessagingRegister(TestCase):
    """TestCase for messaging register view"""
    fixtures = ["fridgify_backend/fixtures/providers.json"]

    def setUp(self):
        """Setup for test case"""
        self.factory = RequestFactory()
        test_utils.create_dummyuser()
        test_utils.create_api_token(timezone.now() + timezone.timedelta(hours=1))

    def test_register_fridgify_exp_201_created(self):
        """Register for Fridgify service. Expecting 201 response"""
        request = self.factory.post(
            "/messaging/register/",
            {"client_token": "firebase_token", "service": 1},
            content_type="application/json"
        )
        request.META["HTTP_AUTHORIZATION"] = "APIToken"

        response = register.register_view(request)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Accesstokens.objects.filter(accesstoken="firebase_token").exists())

    def test_register_hopper_exp_201_create(self):
        """Register for Hopper service. Expecting 201 response"""
        request = self.factory.post(
            "/messaging/register/",
            {"client_token": "hopper_token", "service": 2},
            content_type="application/json"
        )
        request.META["HTTP_AUTHORIZATION"] = "APIToken"

        response = register.register_view(request)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Accesstokens.objects.filter(accesstoken="hopper_token").exists())
