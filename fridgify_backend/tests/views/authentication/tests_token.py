"""Test file for Token"""
# pylint: disable=no-member

import json
from unittest import mock

from django.test import TestCase, RequestFactory
from django.utils import timezone
from rest_framework import status

from fridgify_backend.models import Providers, Accesstokens
from fridgify_backend.views.authentication import token
from fridgify_backend.tests import test_utils


class AuthenticationTestCasesToken(TestCase):
    """TestCase for token view"""
    def setUp(self):
        """Setup for test case"""
        self.factory = RequestFactory()
        test_utils.clean()
        test_utils.setup()
        user = test_utils.create_dummyuser()
        Accesstokens.objects.create(
            user=user,
            accesstoken="Token",
            provider=Providers.objects.get(name="Fridgify"),
            valid_till=timezone.now() + timezone.timedelta(days=1)
        )

    def tearDown(self):
        """Clean after test execution"""
        test_utils.clean()

    @mock.patch("fridgify_backend.utils.token_utils.create_token")
    def test_get_token_authorization_valid_exp_token(self, mock_create_token):
        """Retrieve token with valid token. Expecting token"""
        mock_create_token.return_value = "API Token"
        request = self.factory.get("/auth/token/")
        request.META["HTTP_AUTHORIZATION"] = "Token"
        token_response = token.token_view(request)
        content = token_response.render().content
        self.assertEqual(json.loads(content)["token"], "API Token", "Not the correct token.")

    def test_get_token_invalid_jwt_token_exp_403(self):
        """Retrieve token with invalid token. Expecting 403 response"""
        request = self.factory.post("/auth/token/", )
        request.META["HTTP_AUTHORIZATION"] = \
            "This should be wrong"
        token_response = token.token_view(request)
        self.assertEqual(token_response.status_code, 403)

    def test_error_response(self):
        """Retrieve token with invalid method. Expecting 405 response"""
        request = self.factory.post("/auth/token/")
        request.META["HTTP_AUTHORIZATION"] = "Token"
        error = token.token_view(request)
        self.assertEqual(error.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
