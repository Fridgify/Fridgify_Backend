import jwt
import datetime
from django.utils import timezone
from django.test import TestCase, RequestFactory
from unittest import mock

from Fridgify_Backend.models.users import Users
from Fridgify_Backend.models.providers import Providers
from Fridgify_Backend.models.accesstokens import Accesstokens
from Fridgify_Backend.utils import token_handler


def token_fridgify_api(exp_token, provider):
    Accesstokens.objects.create(accesstoken=exp_token, valid_till=timezone.now(),
                                provider=Providers.objects.filter(name=provider).first(),
                                user=Users.objects.filter(username="dummy_name").first())


class UtilsTestCasesTokenHandler(TestCase):
    def setUp(self):
        self.exp_token = "dummy_token"
        self.factory = RequestFactory()
        Users.objects.create(username="dummy_name", name="Dummy", surname="Name", email="dummy@dumdum.dum",
                             password="$2b$12$1hKYhKg4AU54eyES8qjRYOjInIgObjn0JJ8SlWPOpR9MzKcseMDVS",
                             birth_date=datetime.date(2000, 1, 1))
        Providers.objects.create(name="Fridgify")
        Providers.objects.create(name="Fridgify-API")

    @mock.patch('Fridgify_Backend.utils.token_handler.existing_tokens')
    def test_generateToken_NoExistingTokenAndProviderFridgify_newToken(self, mock_existing_tokens):
        mock_existing_tokens.return_value = None
        token = token_handler.generate_token("dummy_name", "Fridgify")
        self.assertIsNotNone(token)
        dec_token = jwt.decode(token, verify=False)
        self.assertEqual("dummy_name", dec_token["user"])
        self.assertIsNotNone(dec_token["secret"])
        db_token = Accesstokens.objects.filter(accesstoken=token, user__username="dummy_name",
                                               provider__name="Fridgify")
        self.assertEqual(len(db_token), 1)

    @mock.patch('Fridgify_Backend.utils.token_handler.existing_tokens')
    def test_generateToken_NoExistingTokenAndProviderFridgifyAPI_newToken(self, mock_existing_tokens):
        mock_existing_tokens.return_value = None
        token = token_handler.generate_token("dummy_name", "Fridgify-API")
        self.assertIsNotNone(token)
        self.assertEqual(len(token), 64)
        db_token = Accesstokens.objects.filter(accesstoken=token, user__username="dummy_name",
                                               provider__name="Fridgify-API")
        self.assertEqual(len(db_token), 1)

    @mock.patch('Fridgify_Backend.utils.token_handler.existing_tokens')
    def test_generateToken_ExistingTokenFridgify_existingToken(self, mock_existing_tokens):
        provider = "Fridgify"
        Accesstokens.objects.create(accesstoken=self.exp_token, valid_till=timezone.now(),
                                    provider=Providers.objects.filter(name=provider).first(),
                                    user=Users.objects.filter(username="dummy_name").first())
        mock_existing_tokens.return_value = self.exp_token
        token = token_handler.generate_token("dummy_name", provider)
        self.assertEqual(self.exp_token, token)
        db_token = Accesstokens.objects.filter(accesstoken=token, user__username="dummy_name",
                                               provider__name="Fridgify")
        self.assertEqual(len(db_token), 1)

    @mock.patch('Fridgify_Backend.utils.token_handler.existing_tokens')
    def test_generateToken_ExistingTokenFridgifyAPI_existingToken(self, mock_existing_tokens):
        provider = "Fridgify-API"
        token_fridgify_api(self.exp_token, provider)
        mock_existing_tokens.return_value = self.exp_token
        token = token_handler.generate_token("dummy_name", provider)
        self.assertEqual(self.exp_token, token)
        db_token = Accesstokens.objects.filter(accesstoken=token, user__username="dummy_name",
                                               provider__name="Fridgify-API")
        self.assertEqual(len(db_token), 1)

    @mock.patch('Fridgify_Backend.utils.token_handler.is_token_valid')
    def test_existingToken_ValidUserProvider_Token(self, mock_token_valid):
        provider = "Fridgify"
        mock_token_valid.return_value = True
        Accesstokens.objects.create(accesstoken=self.exp_token, valid_till=timezone.now(),
                                    provider=Providers.objects.filter(name=provider).first(),
                                    user=Users.objects.filter(username="dummy_name").first())
        token = token_handler.existing_tokens("dummy_name", provider)
        self.assertEqual(self.exp_token, token)

    def test_existingToken_NotExistingUserProvider_None(self):
        provider = "Fridgify"
        token = token_handler.existing_tokens("dummy_name", provider)
        self.assertEqual(None, token)

    @mock.patch('Fridgify_Backend.utils.token_handler.is_token_valid')
    def test_existingToken_InvalidUserProvider_None(self, mock_token_valid):
        provider = "Fridgify"
        mock_token_valid.return_value = False
        Accesstokens.objects.create(accesstoken=self.exp_token,
                                    valid_till=datetime.datetime(2018, 1, 1, 1, 1, 1, 1, datetime.timezone.utc),
                                    provider=Providers.objects.filter(name=provider).first(),
                                    user=Users.objects.filter(username="dummy_name").first())
        token = token_handler.existing_tokens("dummy_name", provider)
        self.assertEqual(None, token)

    def test_isTokenValid_OutdatedToken_False(self):
        provider = "Fridgify"
        Accesstokens.objects.create(accesstoken=self.exp_token,
                                    valid_till=datetime.datetime(2018, 1, 1, 1, 1, 1, 1,datetime.timezone.utc),
                                    provider=Providers.objects.filter(name=provider).first(),
                                    user=Users.objects.filter(username="dummy_name").first())
        s_obj = Accesstokens.objects.filter(accesstoken=self.exp_token, provider__name=provider, user__username="dummy_name")
        self.assertEqual(1, len(s_obj))
        deleted = token_handler.is_token_valid(s_obj)
        self.assertEqual(deleted, False)
        obj = Accesstokens.objects.filter(accesstoken=self.exp_token, provider__name=provider, user__username="dummy_name")
        self.assertEqual(0, len(obj))

    def test_isTokenValid_ValidToken_False(self):
        provider = "Fridgify"
        Accesstokens.objects.create(accesstoken=self.exp_token,
                                    valid_till=datetime.datetime(2020, 1, 1, 1, 1, 1, 1,datetime.timezone.utc),
                                    provider=Providers.objects.filter(name=provider).first(),
                                    user=Users.objects.filter(username="dummy_name").first())
        s_obj = Accesstokens.objects.filter(accesstoken=self.exp_token, provider__name=provider,
                                            user__username="dummy_name")
        self.assertEqual(1, len(s_obj))
        deleted = token_handler.is_token_valid(s_obj)
        self.assertEqual(deleted, True)
        obj = Accesstokens.objects.filter(accesstoken=self.exp_token, provider__name=provider,
                                          user__username="dummy_name")
        self.assertEqual(1, len(obj))
