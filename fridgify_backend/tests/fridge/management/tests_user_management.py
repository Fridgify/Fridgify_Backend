"""Test file for User Management"""
# pylint: disable=no-member

import json


from django.test import TestCase, RequestFactory
from django.utils import timezone

from fridgify_backend.models import UserFridge
from fridgify_backend.views.fridge.management import users
from fridgify_backend.tests import test_utils
from fridgify_backend.utils import const


class TestUserManagement(TestCase):
    """TestCase for user management view"""
    def setUp(self):
        """Setup for test case"""
        self.factory = RequestFactory()
        test_utils.setup()
        self.user = []
        self.user.append(test_utils.create_dummyuser(
            username="Test User",
            name="Test",
            surname="User",
            email="test@user.de"
        ))
        self.user.append(test_utils.create_dummyuser(
            username="Test User 2",
            name="Test 2",
            surname="User 2",
            email="test@user2.de"
        ))
        self.user.append(test_utils.create_dummyuser(
            username="Test User 3",
            name="Test 3",
            surname="User 3",
            email="test@user3.de"
        ))
        self.fridge = test_utils.create_dummyfridge(name="Test Fridge")

        test_utils.connect_fridge_user(
            username=self.user[0].username,
            fridge=self.fridge.name,
            role=const.Constants.ROLE_OWNER
        )
        test_utils.connect_fridge_user(
            username=self.user[1].username,
            fridge=self.fridge.name,
            role=const.Constants.ROLE_OVERSEER
        )
        test_utils.connect_fridge_user(
            username=self.user[2].username,
            fridge=self.fridge.name,
            role=const.Constants.ROLE_USER
        )

        test_utils.create_login_token(
            timezone.now() + timezone.timedelta(days=1),
            username=self.user[0].username
        )
        test_utils.create_api_token(
            timezone.now() + timezone.timedelta(days=1),
            tok="API Token User1",
            username=self.user[0].username
        )

        test_utils.create_login_token(
            timezone.now() + timezone.timedelta(days=1),
            username=self.user[1].username
        )
        test_utils.create_api_token(
            timezone.now() + timezone.timedelta(days=1),
            tok="API Token User2",
            username=self.user[1].username
        )

        test_utils.create_login_token(
            timezone.now() + timezone.timedelta(days=1),
            username=self.user[2].username
        )
        test_utils.create_api_token(
            timezone.now() + timezone.timedelta(days=1),
            tok="API Token User3",
            username=self.user[2].username
        )
        return super().setUp()

    def test_list_users_exp_success(self):
        """List users successfully. Expecting 200 response"""
        request = self.factory.get(f"/fridge/management/{self.fridge.fridge_id}/users")
        request.META["HTTP_AUTHORIZATION"] = "API Token User1"

        response = users.fridge_users_view(request, self.fridge.fridge_id)

        content = json.loads(response.render().content)

        exp_resp = [
            {
                "user": {
                    "user_id": self.user[0].user_id,
                    "username": "Test User",
                    "name": "Test",
                    "surname": "User",
                    "email": "test@user.de",
                    "birth_date": "2000-10-17"
                },
                "role": "Fridge Owner"
            }, {
                "user": {
                    "user_id": self.user[1].user_id,
                    "username": "Test User 2",
                    "name": "Test 2",
                    "surname": "User 2",
                    "email": "test@user2.de",
                    "birth_date": "2000-10-17"
                },
                "role": "Fridge Overseer"
            }, {
                "user": {
                    "user_id": self.user[2].user_id,
                    "username": "Test User 3",
                    "name": "Test 3",
                    "surname": "User 3",
                    "email": "test@user3.de",
                    "birth_date": "2000-10-17"
                },
                "role": "Fridge User"
            }
        ]
        self.assertEqual(exp_resp, content)
        self.assertEqual(response.status_code, 200)

    def test_edit_role_as_owner_target_overseer_to_user_exp_changed_200(self):
        """Change overseer to user as owner. Expecting 200 response"""
        request = self.factory.patch(
            f"/fridge/management/{self.fridge.fridge_id}/users/{self.user[1].user_id}",
            content_type="application/json",
            data={
                "role": "Fridge User"
            }
        )
        request.META["HTTP_AUTHORIZATION"] = "API Token User1"

        response = users.user_role_view(request, self.fridge.fridge_id, self.user[1].user_id)

        content = json.loads(response.render().content)

        self.assertEqual(response.status_code, 200)

        exp_resp = {
            "user": {
                "user_id": self.user[1].user_id,
                "username": "Test User 2",
                "name": "Test 2",
                "surname": "User 2",
                "email": "test@user2.de",
                "birth_date": "2000-10-17"
            },
            "role": "Fridge User"
        }
        self.assertEqual(content, exp_resp)
        self.assertEqual(2, UserFridge.objects.filter(user_id=self.user[1].user_id).get().role)

        fridge = UserFridge.objects.filter(user_id=self.user[1].user_id).get()
        fridge.role = 1

    def test_edit_role_as_overseer_target_user_to_overseer_exp_changed_200(self):
        """Change user to overseer as user. Expecting 200 response"""
        request = self.factory.patch(
            f"/fridge/management/{self.fridge.fridge_id}/users/{self.user[2].user_id}",
            content_type="application/json",
            data={
                "role": "Fridge Overseer"
            }
        )
        request.META["HTTP_AUTHORIZATION"] = "API Token User2"

        response = users.user_role_view(request, self.fridge.fridge_id, self.user[2].user_id)

        content = json.loads(response.render().content)

        self.assertEqual(response.status_code, 200)

        exp_resp = {
            "user": {
                "user_id": self.user[2].user_id,
                "username": "Test User 3",
                "name": "Test 3",
                "surname": "User 3",
                "email": "test@user3.de",
                "birth_date": "2000-10-17"
            },
            "role": "Fridge Overseer"
        }
        self.assertEqual(content, exp_resp)
        self.assertEqual(1, UserFridge.objects.filter(
            user_id=self.user[2].user_id
        ).get().role)

        fridge = UserFridge.objects.filter(user_id=self.user[2].user_id).get()
        fridge.role = 2

    def test_edit_role_as_overseer_target_owner_exp_forbidden_403(self):
        """Change owner role as overseer. Expecting 403 response"""
        request = self.factory.patch(
            f"/fridge/management/{self.fridge.fridge_id}/users/{self.user[0].user_id}",
            content_type="application/json",
            data={
                "role": "Fridge Overseer"
            }
        )
        request.META["HTTP_AUTHORIZATION"] = "API Token User2"

        response = users.user_role_view(
            request,
            self.fridge.fridge_id,
            self.user[0].user_id
        )

        self.assertEqual(response.status_code, 403)

    def test_edit_role_as_overseer_target_self_exp_failed(self):
        """Change role for self. Expecting 409 response"""
        request = self.factory.patch(
            f"/fridge/management/{self.fridge.fridge_id}/users/{self.user[1].user_id}",
            content_type="application/json",
            data={
                "role": "Fridge User"
            }
        )
        request.META["HTTP_AUTHORIZATION"] = "API Token User2"

        response = users.user_role_view(
            request,
            self.fridge.fridge_id,
            self.user[1].user_id
        )
        self.assertEqual(response.status_code, 409)

    def test_edit_role_unknown_role_exp_role_not_existing_406(self):
        """Change role to unknown role. Expecting 406 response"""
        request = self.factory.patch(
            f"/fridge/management/{self.fridge.fridge_id}/users/{self.user[1].user_id}",
            content_type="application/json",
            data={
                "role": "Fridge This Does Not Exist"
            }
        )
        request.META["HTTP_AUTHORIZATION"] = "API Token User1"

        response = users.user_role_view(request, self.fridge.fridge_id, self.user[1].user_id)
        self.assertEqual(response.status_code, 406)
