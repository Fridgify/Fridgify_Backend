"""Test file for Register"""
# pylint: disable=no-member

from django.test import TestCase, RequestFactory
from rest_framework import status
from fridgify_backend.views.authentication import register
from fridgify_backend.tests import test_utils


class AuthenticationTestCasesRegister(TestCase):
    """TestCase for register view"""
    def setUp(self):
        """Setup for test case"""
        self.factory = RequestFactory()
        test_utils.create_dummyuser()
        test_utils.create_dummyuser("Dummy2", "Not Dummy", "Is", "dumdum@d.de")

    def tearDown(self):
        """Clean after test execution"""
        test_utils.clean()

    def test_register_valid_request_exp_201(self):
        """Register with valid body. Expecting 201 response"""
        request = self.factory.post(
            "/auth/register/",
            {
                "username": "newbie",
                "password": "password2",
                "email": "newbie@nub.de",
                "name": "Newbie",
                "surname": "Noob",
                "birth_date": "2000-12-17"
            },
            content_type="application/json"
        )
        response = register.register_view(request)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_register_invalid_request_exp_400(self):
        """Register with invalid body. Expecting a 400 response"""
        request = self.factory.post(
            "/auth/register/",
            {
                "username": "newbie",
                "password": "password2",
                "birth_date": "2000-12-17"
            },
            content_type="application/json"
        )
        response = register.register_view(request)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_register_username_existing_exp_409(self):
        """Register with existing username. Expecting 409 response"""
        request = self.factory.post(
            "/auth/register/",
            {
                "username": "dummy_name",
                "password": "password",
                "email": "dummy@d.de",
                "name": "Dummy",
                "surname": "Name",
                "birth_date": "2000-12-17"
            },
            content_type="application/json"
        )
        response = register.register_view(request)
        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)

    def test_register_email_existing_409(self):
        """Register with existing email. Expecting 409 response"""
        request = self.factory.post(
            "/auth/register/",
            {
                "username": "dummyDumDam",
                "password": "password",
                "email": "dummy@d.de",
                "name": "Dummy",
                "surname": "Name",
                "birth_date": "2000-12-17"
            },
            content_type="application/json"
        )
        response = register.register_view(request)
        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)
