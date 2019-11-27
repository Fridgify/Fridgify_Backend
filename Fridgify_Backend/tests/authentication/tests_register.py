import json
from unittest import mock
from django.test import TestCase, RequestFactory
from rest_framework import status
from Fridgify_Backend.views.authentication import register
from Fridgify_Backend.tests import test_utils


class AuthenticationTestCasesRegister(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        test_utils.create_dummyuser()

    @mock.patch("Fridgify_Backend.utils.register_handler.register")
    def test_register_ValidRequest_201(self, mock_register):
        mock_register.return_value = 1
        request = self.factory.post("/auth/register", {"username": "newbie", "password": "password2",
                                                       "email": "newbie@nub.de", "name": "Newbie", "surname": "Noob",
                                                       "birthdate": "2000-12-17"}, content_type="application/json")
        response = register.register(request)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    @mock.patch("Fridgify_Backend.utils.register_handler.register")
    def test_register_InvalidRequest_400(self, mock_register):
        mock_register.return_value = 0
        request = self.factory.post("/auth/register", {"username": "newbie", "password": "password2",
                                                       "birthdate": "2000-12-17"}, content_type="application/json")
        response = register.register(request)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @mock.patch("Fridgify_Backend.utils.register_handler.register")
    def test_register_DatabaseError_500(self, mock_register):
        mock_register.return_value = -1
        request = self.factory.post("/auth/register", {"username": "newbie", "password": "password2",
                                                       "birthdate": "2000-12-17"}, content_type="application/json")
        response = register.register(request)
        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)

    @mock.patch("Fridgify_Backend.utils.register_handler.register")
    def test_register_UsernameExisting_409(self, mock_register):
        mock_register.return_value = -2
        request = self.factory.post("/auth/register", {"username": "dummy_name", "password": "password",
                                                       "email": "dummy@d.de", "name": "Dummy", "surname": "Name",
                                                       "birthdate": "2000-12-17"}, content_type="application/json")
        response = register.register(request)
        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)

    @mock.patch("Fridgify_Backend.utils.register_handler.register")
    def test_register_EmailExisting_409(self, mock_register):
        mock_register.return_value = -3
        request = self.factory.post("/auth/register", {"username": "dummyDumDam", "password": "password",
                                                       "email": "dummy@d.de", "name": "Dummy", "surname": "Name",
                                                       "birthdate": "2000-12-17"}, content_type="application/json")
        response = register.register(request)
        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)
