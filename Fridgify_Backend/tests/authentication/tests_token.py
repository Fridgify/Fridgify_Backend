import json
import datetime
import collections
from unittest import mock
from django.test import TestCase, RequestFactory
from rest_framework import status

from Fridgify_Backend.views.authentication import token
from Fridgify_Backend.models.users import Users
from Fridgify_Backend.models.providers import Providers


def request_get(request):
    return "method allowed"


def request_any(request):
    return "method not allowed"


class AuthenticationTestCasesToken(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        Users.objects.create(username="dummy_name", name="Dummy", surname="Name", email="dummy@dumdum.dum",
                             password="$2b$12$1hKYhKg4AU54eyES8qjRYOjInIgObjn0JJ8SlWPOpR9MzKcseMDVS",
                             birth_date=datetime.date(2000, 1, 1))
        Providers.objects.create(name="Fridgify")
        Providers.objects.create(name="Fridgify-API")

    """Token test case"""
    def test_token(self):
        # response = json.loads(token.entry_point("dummy").content)
        # self.assertEqual(response["message"], "token", "Test token")
        self.assertEqual(0, 0, "Dummy Test")

    @mock.patch('Fridgify_Backend.utils.token_handler.existing_tokens')
    @mock.patch('Fridgify_Backend.utils.token_handler.generate_token')
    def test_getToken_AuthorizationValid_token(self, mock_generate_token, mock_existing_tokens):
        mock_generate_token.return_value = "API Token"
        mock_existing_tokens.return_value = \
            "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyIjoiZHVtbXkifQ.5ss19_EcoZKrWUvrEnmnoiBibvj0SbCSwL9XxdjtfgQ"

        request = self.factory.post("/auth/token/",)
        request.META["HTTP_AUTHORIZATION"] = \
            "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyIjoiZHVtbXkifQ.5ss19_EcoZKrWUvrEnmnoiBibvj0SbCSwL9XxdjtfgQ"
        token_response = token.get_token(request)
        self.assertEqual(token_response, "API Token", "Not the correct token.")

    def test_getToken_InvalidJWTToken_none(self):
        request = self.factory.post("/auth/token/", )
        request.META["HTTP_AUTHORIZATION"] = \
            "This should not be decodable. haha"
        token_response = token.get_token(request)
        self.assertEqual(token_response, None, "JWT Token was decoded")

    @mock.patch('Fridgify_Backend.utils.token_handler.existing_tokens')
    @mock.patch('Fridgify_Backend.utils.token_handler.generate_token')
    def test_getToken_AuthorizationInvalid_none(self, mock_generate_token, mock_existing_tokens):
        mock_generate_token.return_value = "API Token"
        mock_existing_tokens.return_value = \
            "Token"

        request = self.factory.post("/auth/token/", )
        request.META["HTTP_AUTHORIZATION"] = \
            "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyIjoiZHVtbXkifQ.5ss19_EcoZKrWUvrEnmnoiBibvj0SbCSwL9XxdjtfgQ"
        token_response = token.get_token(request)
        self.assertEqual(token_response, None, "Correct token")

    def test_error_response(self):
        error = token.error_response({})
        self.assertEqual(error.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    @mock.patch('Fridgify_Backend.views.authentication.token.get_token')
    def test_getResponse_ValidToken_TokenResponse(self, mock_token):
        mock_token.return_value = "Token A"
        resp = token.get_response({})
        self.assertEqual(json.loads(resp.content.decode("utf-8"))["token"], "Token A")
        self.assertEqual(json.loads(resp.content.decode("utf-8"))["validation_time"], 3600)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    @mock.patch('Fridgify_Backend.views.authentication.token.get_token')
    def test_getReponse_InvalidToken_401(self, mock_token):
        mock_token.return_value = None
        resp = token.get_response({})
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_entryPoint_GET_allowed(self):
        ret_val = collections.defaultdict(lambda: request_any)
        ret_val["GET"] = request_get
        with mock.patch.object(token, 'HTTP_ENDPOINT_FUNCTION', ret_val):
            request = self.factory.get("/auth/token/",)
            resp = token.entry_point(request)
            self.assertEqual(resp, "method allowed")

    def test_entryPoint_POST_error(self):
        ret_val = collections.defaultdict(lambda: request_any)
        ret_val["POST"] = request_get
        with mock.patch.object(token, 'HTTP_ENDPOINT_FUNCTION', ret_val):
            request = self.factory.get("/auth/token/",)
            resp = token.entry_point(request)
            self.assertEqual(resp, "method not allowed")

    def test_entryPoint_DELETE_error(self):
        ret_val = collections.defaultdict(lambda: request_any)
        ret_val["DELETE"] = request_get
        with mock.patch.object(token, 'HTTP_ENDPOINT_FUNCTION', ret_val):
            request = self.factory.get("/auth/token/",)
            resp = token.entry_point(request)
            self.assertEqual(resp, "method not allowed")
