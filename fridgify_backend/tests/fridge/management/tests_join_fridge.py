"""Test file for Join Fridge"""
# pylint: disable=no-member

from django.test import TestCase, RequestFactory
from django.utils import timezone

from fridgify_backend.models import UserFridge, Accesstokens
from fridgify_backend.views.fridge.management import join_fridge
from fridgify_backend.tests import test_utils


class ManagementTestCasesJoinFridge(TestCase):
    """TestCase for join fridge view"""
    def setUp(self) -> None:
        """Setup for test case"""
        self.factory = RequestFactory()
        test_utils.setup()
        self.user = test_utils.create_dummyuser()
        self.user2 = test_utils.create_dummyuser(
            username="User2",
            email="user2@mail.de"
        )
        self.fridge = test_utils.create_dummyfridge()
        test_utils.connect_fridge_user()
        test_utils.create_login_token(
            timezone.now() + timezone.timedelta(days=1),
            username=self.user.username
        )
        test_utils.create_api_token(
            timezone.now() + timezone.timedelta(days=1),
            tok="API Token",
            username=self.user2.username
        )
        test_utils.create_api_token(
            timezone.now() + timezone.timedelta(days=1),
            tok="Already in Fridge",
            username=self.user.username
        )

        self.token = "jointoken"
        test_utils.create_join_token(tok=self.token, fridge=self.fridge)
        self.s_request = self.factory.get(f"/fridge/management/join?token={self.token}")
        self.s_request.META["HTTP_AUTHORIZATION"] = "API Token"

    def test_valid_join_token_exp_201_created(self):
        """Join fridge with valid token. Expecting 201 response"""
        response = join_fridge.join_view(self.s_request)
        self.assertEqual(response.status_code, 201)

        fridge = UserFridge.objects.filter(
            user_id=self.user.user_id,
            fridge_id=self.fridge.fridge_id
        )
        self.assertTrue(fridge.exists())

    def test_no_join_token_exp_400_bad_request(self):
        """Join fridge with no token. Expecting 400 response"""
        request = self.factory.get("/fridge/management/join")
        request.META["HTTP_AUTHORIZATION"] = "API Token"
        response = join_fridge.join_view(request)
        self.assertEqual(response.status_code, 400)

    def test_join_token_not_existent_exp_404_not_found(self):
        """Join fridge with no existing token. Expecting 404 response"""
        request = self.factory.get(
            "/fridge/management/join?token=ThisShouldAbsolutelyNotWork"
        )
        request.META["HTTP_AUTHORIZATION"] = "API Token"
        response = join_fridge.join_view(request)
        self.assertEqual(response.status_code, 404)

    def test_join_token_already_in_fridge_exp_409_conflict(self):
        """Join fridge, already a member. Expecting 409 response"""
        request = self.factory.get(f"/fridge/management/join?token={self.token}")
        request.META["HTTP_AUTHORIZATION"] = "Already in Fridge"
        response = join_fridge.join_view(request)
        self.assertEqual(response.status_code, 409)

    def test_link_not_valid_exp_410_gone(self):
        """Join fridge, where token is expired. Expecting 410 response"""
        token = Accesstokens.objects.get(
            provider__name="Fridgify-Join",
            accesstoken=self.token,
            fridge=self.fridge,
            user=self.user
        )
        token.valid_till = timezone.now() - timezone.timedelta(days=15)
        token.save()

        response = join_fridge.join_view(self.s_request)
        self.assertEqual(response.status_code, 410)
        self.assertFalse(Accesstokens.objects.filter(
            provider__name="Fridgify-Join",
            accesstoken=self.token,
            fridge=self.fridge,
            user=self.user
        ).exists())

        test_utils.create_join_token(tok=self.token, fridge=self.fridge)
