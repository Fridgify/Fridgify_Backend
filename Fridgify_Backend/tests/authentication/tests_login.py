import json
import collections
import datetime
from django.utils import timezone
from django.test import RequestFactory, TestCase
from unittest import mock
from rest_framework import status

from Fridgify_Backend.views.authentication import login
from Fridgify_Backend.models.users import Users
from Fridgify_Backend.models.providers import Providers
from Fridgify_Backend.models.accesstokens import Accesstokens


def request_post(request):
    return "login_method"


def request_any(request):
    return "error_method"


class AuthenticationTestCasesLogin(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        Users.objects.create(username="dummy_name", name="Dummy", surname="Name", email="dummy@dumdum.dum",
                             password="$2b$12$1hKYhKg4AU54eyES8qjRYOjInIgObjn0JJ8SlWPOpR9MzKcseMDVS",
                             birth_date=datetime.date(2000, 1, 1))
        Providers.objects.create(name="Fridgify")
        Providers.objects.create(name="Fridgify-API")
        Accesstokens.objects.create(accesstoken="Token", provider=Providers.objects.filter(name="Fridgify").first(),
                                    valid_till=timezone.now() + datetime.timedelta(days=14),
                                    user=Users.objects.filter(username="dummy_name").first())

    @mock.patch('Fridgify_Backend.utils.login_handler.check_credentials')
    @mock.patch('Fridgify_Backend.utils.token_handler.generate_token')
    def test_login_ValidCredentials_Token(self, mock_generate_token, mock_check_credentials):
        mock_check_credentials.return_value = 1
        mock_generate_token.return_value = "A Token"
        request = self.factory.post("/auth/login/", {"username": "dummy_name", "password": "password"},
                                    content_type="application/json")
        response = login.login(request)
        j_response = json.loads(response.content.decode("utf-8"))
        self.assertEqual(j_response["token"], "A Token", "Token was not send")

    @mock.patch('Fridgify_Backend.utils.login_handler.check_credentials')
    def test_login_InvalidCredentials_401(self, mock_check_credentials):
        mock_check_credentials.return_value = 0
        request = self.factory.post("/auth/login/", {"username": "dummy_name", "password": "lol wrong pw"},
                                    content_type="application/json")
        response = login.login(request)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED, "User is not unauthorized...")

    @mock.patch('Fridgify_Backend.utils.login_handler.check_credentials')
    def test_login_InvalidRequest_400(self, mock_check_credentials):
        mock_check_credentials.return_value = -1
        request = self.factory.post("/auth/login/", {"username": "dummy_name"},
                                    content_type="application/json")
        response = login.login(request)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST, "Not a bad request")

    @mock.patch('Fridgify_Backend.utils.token_handler.existing_tokens')
    def test_login_AuthorizationTokenValid_Token(self, mock_existing_token):
        mock_existing_token.return_value = "Token"
        request = self.factory.post("/auth/login/", {"username": "dummy_name", "password": "lol wrong pw"},
                                    content_type="application/json", )
        request.META["HTTP_AUTHORIZATION"] = "Token"
        response = login.login(request)
        self.assertEqual(json.loads(response.content)["token"], "Token",
                         "Authorization header not respected")

    @mock.patch('Fridgify_Backend.utils.token_handler.existing_tokens')
    def test_login_AuthorizationTokenInvalid_401(self, mock_existing_token):
        mock_existing_token.return_value = None
        request = self.factory.post("/auth/login/", {"username": "dummy_name", "password": "lol wrong pw"},
                                    content_type="application/json", )
        request.META["HTTP_AUTHORIZATION"] = "Absolutely wrong"
        response = login.login(request)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED, "Token not invalid")

    def test_errorResponse_N_response(self):
        response = login.error_response({})
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED, "Wrong method was allowed")
        self.assertEqual(response["Allow"], "POST", "Not POST")

    def test_entryPoint_POST_method(self):
        ret_val = collections.defaultdict(lambda: request_post)
        ret_val["POST"] = request_post
        with mock.patch.object(login, 'HTTP_ENDPOINT_FUNCTION', ret_val):
            request = self.factory.post("/auth/login/", {"username": "dummy_name", "password": "lol wrong pw"},
                                        content_type="application/json", )
            resp = login.entry_point(request)
            self.assertEqual(resp, "login_method")

    def test_entryPoint_GET_error(self):
        ret_val = collections.defaultdict(lambda: request_post)
        ret_val["GET"] = request_any
        with mock.patch.object(login, 'HTTP_ENDPOINT_FUNCTION', ret_val):
            request = self.factory.get("/auth/login/",)
            resp = login.entry_point(request)
            self.assertEqual(resp, "error_method")

    def test_entryPoint_DELETE_error(self):
        ret_val = collections.defaultdict(lambda: request_post)
        ret_val["DELETE"] = request_any
        with mock.patch.object(login, 'HTTP_ENDPOINT_FUNCTION', ret_val):
            request = self.factory.delete("/auth/login/",)
            resp = login.entry_point(request)
            self.assertEqual(resp, "error_method")
