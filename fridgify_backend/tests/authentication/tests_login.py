import json
import collections
import datetime
from django.utils import timezone
from django.test import RequestFactory, TestCase
from unittest import mock
from rest_framework import status

from fridgify_backend.views.authentication import login
from fridgify_backend.models import Users, Providers, Accesstokens
from fridgify_backend.tests import test_utils


class AuthenticationTestCasesLogin(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        test_utils.setup()
        test_utils.create_dummyuser()
        Accesstokens.objects.create(accesstoken="Token", provider=Providers.objects.filter(name="Fridgify").first(),
                                    valid_till=timezone.now() + datetime.timedelta(days=14),
                                    user=Users.objects.filter(username="dummy_name").first())

    def tearDown(self) -> None:
        test_utils.clean()

    def test_login_ValidCredentials_Token(self):
        request = self.factory.post("/auth/login/", {"username": "dummy_name", "password": "password"},
                                    content_type="application/json")
        response = login.login_view(request)
        j_response = json.loads(response.render().content.decode("utf-8"))
        self.assertEqual(j_response["token"], "Token", "Token was not send")

    def test_login_InvalidCredentials_401(self):
        request = self.factory.post("/auth/login/", {"username": "dummy_name", "password": "lol wrong pw"},
                                    content_type="application/json")
        response = login.login_view(request)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN, "User is not unauthorized...")

    def test_login_InvalidRequest_400(self):
        request = self.factory.post("/auth/login/", {"username": "dummy_name"},
                                    content_type="application/json")
        response = login.login_view(request)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST, "Not a bad request")

    def test_login_AuthorizationTokenValid_Token(self):
        request = self.factory.post("/auth/login/", {"username": "dummy_name", "password": "lol wrong pw"},
                                    content_type="application/json", )
        request.META["HTTP_AUTHORIZATION"] = "Token"
        response = login.login_view(request)
        self.assertEqual(json.loads(response.render().content)["token"], "Token",
                         "Authorization header not respected")

    def test_login_AuthorizationTokenInvalid_403(self):
        request = self.factory.post("/auth/login/", {"username": "dummy_name", "password": "lol wrong pw"},
                                    content_type="application/json", )
        request.META["HTTP_AUTHORIZATION"] = "Absolutely wrong"
        response = login.login_view(request)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN, "Token not invalid")

    def test_wrong_method(self):
        request = self.factory.get("/auth/login/")
        response = login.login_view(request)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED, "Wrong method was allowed")
