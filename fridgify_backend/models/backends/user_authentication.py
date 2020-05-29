import json
import logging

import bcrypt
from django.utils import timezone
from rest_framework import authentication
from rest_framework import exceptions

from fridgify_backend.models import Users, Accesstokens
from fridgify_backend.utils.decorators import check_body


logger = logging.getLogger(__name__)


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
        try:
            credentials = json.loads(request.body.decode("utf-8"))
            logger.info(f"Authenticate user {credentials['username']} via credentials...")
            try:
                user = Users.objects.get(username=credentials["username"])
            except Users.DoesNotExist:
                logger.error(f"User {credentials['username']} does not exist...")
                raise exceptions.AuthenticationFailed()

            if bcrypt.checkpw(credentials["password"].encode("utf-8"), user.password.encode("utf-8")):
                user.is_authenticated = True
                return user, None
            else:
                logger.warning(f"User {credentials['username']} not authenticated...")
                raise exceptions.AuthenticationFailed
        except json.JSONDecodeError:
            logger.error(f"Couldn't parse JSON:\n {request.body.decode('utf-8')}")
            raise exceptions.ParseError()

    @staticmethod
    def authenticate_token(req_token):
        """
        Authentication via login token
        :param req_token: Login-Token
        :return: (user instance, None)
        """
        try:
            logger.info(f"Authenticate via token {req_token}")
            token = Accesstokens.objects.get(
                accesstoken=req_token,
                provider__name="Fridgify",
                valid_till__gte=timezone.now()
            )
            token.user.is_authenticated = True
            token.user.token_authentication = token.accesstoken
            return token.user, None
        except Accesstokens.DoesNotExist or Accesstokens.MultipleObjectsReturned:
            logger.error("Token does not exist...")
            raise exceptions.AuthenticationFailed
