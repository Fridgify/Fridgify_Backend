import secrets
import jwt
import datetime
from django.utils import timezone
import json

from Fridgify_Backend.models.accesstokens import Accesstokens
from Fridgify_Backend.models.providers import Providers
from Fridgify_Backend.models.users import Users


def generate_token(username, internal_provider):
    """ Generate a token for our internal providers

    :param username: username
    :param internal_provider: Either Fridgify or Fridgify-API
    :return: Generic Token
    """
    print("Generating token for internal provider...")
    # Retrieve existing tokens, wipe outdated tokens
    token = existing_tokens(username, internal_provider)

    # If no token existing, create a new one
    if token is None:
        client_secret = ""
        if internal_provider == "Fridgify":
            client_secret = secrets.token_hex(8)
            token = jwt.encode(payload={"user": username, "secret": client_secret}, key=client_secret,
                               algorithm="HS256").decode("utf-8")
        else:
            token = secrets.token_hex(32)

        db_token = Accesstokens()
        db_token.accesstoken = token
        db_token.provider = Providers.objects.filter(name=internal_provider).first()
        if internal_provider == "Fridgify":
            db_token.valid_till = timezone.now() + timezone.timedelta(days=14)
        else:
            db_token.valid_till = timezone.now() + timezone.timedelta(hours=1)
        db_token.user = Users.objects.filter(username=username).first()
        db_token.client_id = username
        db_token.client_secret = client_secret
        db_token.save()

    return token


def existing_tokens(username, internal_provider):
    """ Check if a token already exists

    :param username: name of user
    :param internal_provider: Either Fridgify or Fridgify-API
    :return: existing token or none
    """
    print("Check if token already exists...")
    token_objs = Accesstokens.objects.filter(user__username=username, provider__name=internal_provider)
    if len(token_objs) > 0:
        if is_token_valid(token_objs):
            return token_objs.values("accesstoken").first()["accesstoken"]
        else:
            return None


def is_token_valid(token_objs):
    """ Check if a token is still valid

    :param token_objs: Entries matching user and provider
    :return: valid - True | invalid - False
    """
    print("Check validity of token...")
    valid_till = token_objs.values_list("valid_till").first()

    if timezone.now() > valid_till[0]:
        token_objs.first().delete()
        return False
    else:
        return True
