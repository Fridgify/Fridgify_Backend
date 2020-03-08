import json
import time

import bcrypt
from rest_framework import authentication
from rest_framework import exceptions

from Fridgify_Backend.models import Users, Accesstokens


class UserAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        if "Authorization" in request.headers:
            return self.authenticate_token(request.headers["Authorization"])
        else:
            credentials = json.loads(request.body)
            return self.authenticate_credentials(credentials["username"], credentials["password"])

    @staticmethod
    def authenticate_credentials(username, password):
        try:
            user = Users.objects.get(username=username)
        except Users.DoesNotExist:
            pass

        if bcrypt.checkpw(password, user.password):
            return user, None
        else:
            return exceptions.AuthenticationFailed

    @staticmethod
    def authenticate_token(self, token):
        try:
            token = Accesstokens.objects.get(
                accesstoken=token,
                provider="Fridgify",
                valid_till__gte=time.time()
            )
            return token.user, None
        except Accesstokens.DoesNotExist or Accesstokens.MultipleObjectsReturned:
            return exceptions.AuthenticationFailed
