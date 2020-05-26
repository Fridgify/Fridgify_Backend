import json

import bcrypt
from rest_framework import authentication
from rest_framework import exceptions
from django.utils import timezone

from Fridgify_Backend.models import Users, Accesstokens
from Fridgify_Backend.utils.decorators import check_body


class UserAuthentication(authentication.BaseAuthentication):
    """
    Backend is responsible for authenticating the user during the login process.
    If the request header contains "Authorization", a valid Login-Token is required. Otherwise the request body should
    have username and password.
    """
    def authenticate(self, request):
        if "Authorization" in request.headers:
            return self.authenticate_token(request.headers["Authorization"])
        else:
            if request.method != "GET":
                return self.authenticate_credentials(request)

    @staticmethod
    @check_body("username", "password")
    def authenticate_credentials(request):
        """
        Authentication check via user credentials
        :param request
        :return: (user instance, None)
        """
        body = request.body.decode("utf-8")
        try:
            credentials = json.loads(body)
            try:
                user = Users.objects.get(username=credentials["username"])
            except Users.DoesNotExist:
                raise exceptions.AuthenticationFailed()

            if bcrypt.checkpw(credentials["password"].encode("utf-8"), user.password.encode("utf-8")):
                user.is_authenticated = True
                return user, None
            else:
                raise exceptions.AuthenticationFailed
        except json.JSONDecodeError:
            pass

    @staticmethod
    def authenticate_token(req_token):
        """
        Authentication via login token
        :param req_token: Login-Token
        :return: (user instance, None)
        """
        try:
            token = Accesstokens.objects.get(
                accesstoken=req_token,
                provider__name="Fridgify",
                valid_till__gte=timezone.now()
            )
            token.user.is_authenticated = True
            token.user.token_authentication = token.accesstoken
            return token.user, None
        except Accesstokens.DoesNotExist or Accesstokens.MultipleObjectsReturned:
            raise exceptions.AuthenticationFailed
