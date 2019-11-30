import datetime
from django.test import TestCase, RequestFactory
from unittest import mock

from Fridgify_Backend.utils import login_handler
from Fridgify_Backend.models.users import Users
from Fridgify_Backend.models.providers import Providers


class UtilsTestCasesLoginHandler(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        Users.objects.create(username="dummy_name", name="Dummy", surname="Name", email="dummy@dumdum.dum",
                             password="$2b$12$1hKYhKg4AU54eyES8qjRYOjInIgObjn0JJ8SlWPOpR9MzKcseMDVS",
                             birth_date=datetime.date(2000, 1, 1))
        Providers.objects.create(name="Fridgify")
        Providers.objects.create(name="Fridgify-API")

    @mock.patch('Fridgify_Backend.utils.login_handler.retrieve_password')
    def test_checkCredentials_ValidCredentials_1(self, mock_retrieve_password):
        mock_retrieve_password.return_value = "$2b$12$1hKYhKg4AU54eyES8qjRYOjInIgObjn0JJ8SlWPOpR9MzKcseMDVS"
        request = self.factory.post("/auth/login/", {"username": "dummy_name", "password": "password"},
                                    content_type="application/json")
        auth = login_handler.check_credentials(request)
        self.assertEqual(1, auth)

    @mock.patch('Fridgify_Backend.utils.login_handler.retrieve_password')
    def test_checkCredentials_InvalidCredentials_1(self, mock_retrieve_password):
        mock_retrieve_password.return_value = "$2b$12$1hKYhKg4AU54eyES8qjRYOjInIgObjn0JJ8SlWPOpR9MzKcseMDVS"
        request = self.factory.post("/auth/login/", {"username": "dummy_name", "password": "notapassword"},
                                    content_type="application/json")
        auth = login_handler.check_credentials(request)
        self.assertEqual(0, auth)

    def test_checkCredentials_MissingUsername_minus1(self):
        request = self.factory.post("/auth/login/", {"password": "password"},
                                    content_type="application/json")
        auth = login_handler.check_credentials(request)
        self.assertEqual(-1, auth)

    @mock.patch('Fridgify_Backend.utils.login_handler.retrieve_password')
    def test_checkCredentials_NothingFound_0(self, mock_retrieve_password):
        mock_retrieve_password.return_value = "$2b$12$1hKYhKg4lo9Bd4jES8qjRYOjInaIObjn0JJ8SlWPOpR9MzKcseMDVS"
        request = self.factory.post("/auth/login/", {"username": "imnotexistingslol", "password": "password"},
                                    content_type="application/json")
        auth = login_handler.check_credentials(request)
        self.assertEqual(0, auth)

    @mock.patch('Fridgify_Backend.utils.login_handler.retrieve_password')
    def test_checkCredentials_Mail_Password(self, mock_retrieve_password):
        mock_retrieve_password.return_value = "$2b$12$1hKYhKg4AU54eyES8qjRYOjInIgObjn0JJ8SlWPOpR9MzKcseMDVS"
        request = self.factory.post("/auth/login/", {"username": "dummy@dumdum.dum", "password": "password"},
                                    content_type="application/json")
        auth = login_handler.check_credentials(request)
        self.assertEqual(1, auth)

    @mock.patch('Fridgify_Backend.utils.login_handler.retrieve_password')
    def test_checkCredentials_WrongMail_Password(self, mock_retrieve_password):
        mock_retrieve_password.return_value = None
        request = self.factory.post("/auth/login/", {"username": "dummy@dumdum.dum", "password": "password"},
                                    content_type="application/json")
        auth = login_handler.check_credentials(request)
        self.assertEqual(0, auth)

    def test_retrievePassword_UsernameExists_Password(self):
        password = login_handler.retrieve_password("dummy_name")
        self.assertEqual("$2b$12$1hKYhKg4AU54eyES8qjRYOjInIgObjn0JJ8SlWPOpR9MzKcseMDVS", password)

    def test_retrievePassword_EmailExists_Password(self):
        password = login_handler.retrieve_password("dummy@dumdum.dum")
        self.assertEqual("$2b$12$1hKYhKg4AU54eyES8qjRYOjInIgObjn0JJ8SlWPOpR9MzKcseMDVS", password)

    def test_retrievePassword_UsernameNotExisting_NoPassword(self):
        password = login_handler.retrieve_password("NotAUser")
        self.assertEqual(None, password)

    def test_retrievePassword_EmailNotExisting_NoPassword(self):
        password = login_handler.retrieve_password("NotAEmail")
        self.assertEqual(None, password)
