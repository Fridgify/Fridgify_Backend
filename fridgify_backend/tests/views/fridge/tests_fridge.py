"""Test file for Fridge"""
# pylint: disable=no-member

import datetime

from django.test import TestCase, RequestFactory

from fridgify_backend.models import Users, Fridges, UserFridge
from fridgify_backend.tests.test_utils import fill_fridges
from fridgify_backend.tests import test_utils


class ManagementTestCasesCreateFridge(TestCase):
    """TestCase for create fridge view"""
    def setUp(self):
        """Setup for test case"""
        test_utils.setup()
        self.factory = RequestFactory()
        self.user = Users.objects.create(
            username="dummy_name",
            name="Dummy",
            surname="Name",
            email="dummy@dumdum.dum",
            password="$2b$12$1hKYhKg4AU54eyES8qjRYOjInIgObjn0JJ8SlWPOpR9MzKcseMDVS",
            birth_date=datetime.date(2000, 1, 1)
        )
        self.user2 = Users.objects.create(
            username="testUser",
            name="Test",
            surname="User",
            email="test@user.dum",
            password="$2b$12$1hKYhKg4AU54eyES8qjRYOjInIgObjn0JJ8SlWPOpR9MzKcseMDVS",
            birth_date=datetime.date(2000, 1, 1)
        )
        fridge = Fridges.objects.create(name="Miau", description="adsdsadad")
        fill_fridges([fridge])
        fridge2 = Fridges.objects.create(name="Wuff", description="adsdsadad")
        UserFridge.objects.create(fridge_id=fridge.fridge_id, user_id=self.user.user_id)
        UserFridge.objects.create(fridge_id=fridge2.fridge_id, user_id=self.user2.user_id)

    def test_user_1_has_1_fridge(self):
        """User A created only one fridge"""
        fridges = UserFridge.objects.filter(user_id=self.user.user_id)
        self.assertEqual(len(fridges), 1, "User has more than one fridge")

    def test_user_1_has_the_correct_fridge(self):
        """User A created the expected fridge"""
        user_fridges = UserFridge.objects.filter(user_id=self.user.user_id)
        for user_fridge in user_fridges:
            fridge = Fridges.objects.get(fridge_id=user_fridge.fridge_id)
            self.assertEqual(fridge.name, "Miau", "User has the wrong fridge")

    def test_user_2_has_1_fridge(self):
        """User B created only one fridge"""
        fridges = UserFridge.objects.filter(user_id=self.user.user_id)
        self.assertEqual(len(fridges), 1, "User2 has more than one fridge")

    def test_user_2_has_the_correct_fridge(self):
        """User B created the expected fridge"""
        user_fridges = UserFridge.objects.filter(user_id=self.user2.user_id)
        for user_fridge in user_fridges:
            fridge = Fridges.objects.get(fridge_id=user_fridge.fridge_id)
            self.assertEqual(fridge.name, "Wuff", "User2 has the wrong fridge")

    def fridge_content_total_is_not_less_than_sum(self):
        """Total content should be correct"""
        fridges = UserFridge.objects.filter(user_id=self.user.user_id)
        for fridge in fridges:
            self.assertGreaterEqual(
                fridge.content.fresh + fridge.content.overDue + fridge.content.dueSoon,
                fridge.content.total,
                "Fridge content calculation is off. "
                "Total has to be more than or equal the sum off fresh, "
                "overDue and dueSoon"
            )
