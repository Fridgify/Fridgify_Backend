"""Test file for Subscribing to Messaging Services"""
# pylint: disable=no-member

import json
from unittest.mock import patch

from django.utils import timezone
from django.test import TestCase, RequestFactory
from rest_framework import status

from fridgify_backend.models import Accesstokens
from fridgify_backend.tests import test_utils
from fridgify_backend.views.messaging import subscribe


class TestCaseSubscribeMessaging(TestCase):
    """TestCase for messaging subscription view"""
    fixtures = ["fridgify_backend/fixtures/providers.json"]

    def setUp(self):
        """Setup for test case"""
        self.factory = RequestFactory()
        test_utils.create_dummyuser()
        test_utils.create_api_token(timezone.now() + timezone.timedelta(hours=1))

    def test_subscribe_fridgify_exp_200(self):
        request = self.factory.get("/messaging/subscribe?service=1")
        request.META["HTTP_AUTHORIZATION"] = "APIToken"

        response = subscribe.subscribe_view(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @patch("fridgify_backend.utils.dynamic_link.create_deep_link")
    @patch("fridgify_backend.utils.messaging.hopper.hopper.subscribe")
    def test_subscribe_hopper_exp_200(self, mock_subscribe, mock_dynamic_link):
        request = self.factory.get("/messaging/subscribe?service=2")
        request.META["HTTP_AUTHORIZATION"] = "APIToken"

        mock_dynamic_link.return_value = "https://link.com"
        mock_subscribe.return_value = "https://subscribe.here"

        response = subscribe.subscribe_view(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        body = json.loads(response.render().content)
        self.assertTrue("subscribe_url" in body)
        self.assertEqual(body["subscribe_url"], "https://subscribe.here")

    def test_subscribe_no_service_exp_400(self):
        request = self.factory.get("/messaging/subscribe")
        request.META["HTTP_AUTHORIZATION"] = "APIToken"

        response = subscribe.subscribe_view(request)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_subscribe_non_numeric_service_exp_400(self):
        request = self.factory.get("/messaging/subscribe?service=test")
        request.META["HTTP_AUTHORIZATION"] = "APIToken"

        response = subscribe.subscribe_view(request)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
