import json

import bcrypt
from rest_framework import authentication
from rest_framework import exceptions
from django.utils import timezone

from Fridgify_Backend.models import Users, Accesstokens


class UserAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        if "Authorization" in request.headers:
            return self.authenticate_token(request.headers["Authorization"])
        else:
            if request.method != "GET":
                body = request.body.decode("utf-8")
                credentials = json.loads(body)
                return self.authenticate_credentials(credentials["username"], credentials["password"])

    @staticmethod
    def authenticate_credentials(username, password):
        try:
            user = Users.objects.get(username=username)
        except Users.DoesNotExist:
            raise exceptions.AuthenticationFailed()

        if bcrypt.checkpw(password.encode("utf-8"), user.password.encode("utf-8")):
            user.is_authenticated = True
            return user, None
        else:
            return exceptions.AuthenticationFailed

    @staticmethod
    def authenticate_token(req_token):
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
