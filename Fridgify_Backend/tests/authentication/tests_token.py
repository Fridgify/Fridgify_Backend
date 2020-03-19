import json
import datetime
import collections

from django.test import TestCase, RequestFactory
from django.utils import timezone
from unittest import mock
from rest_framework import status

from Fridgify_Backend.models import Providers, Users, Accesstokens
from Fridgify_Backend.views.authentication import token
from Fridgify_Backend.tests import test_utils


def request_get(request):
    return "method allowed"


def request_any(request):
    return "method not allowed"


class AuthenticationTestCasesToken(TestCase):
    def setUp(self):
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
        test_utils.clean()

    @mock.patch("Fridgify_Backend.utils.token_utils.create_token")
    def test_getToken_AuthorizationValid_token(self, mock_create_token):
        mock_create_token.return_value = "API Token"
        request = self.factory.get("/auth/token/")
        request.META["HTTP_AUTHORIZATION"] = "Token"
        token_response = token.token_view(request)
        content = token_response.render().content
        self.assertEqual(json.loads(content)["token"], "API Token", "Not the correct token.")

    def test_getToken_InvalidJWTToken_none(self):
        request = self.factory.post("/auth/token/", )
        request.META["HTTP_AUTHORIZATION"] = \
            "This should be wrong"
        token_response = token.token_view(request)
        self.assertEqual(token_response.status_code, 403)

    def test_error_response(self):
        request = self.factory.post("/auth/token/")
        error = token.token_view(request)
        self.assertEqual(error.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
