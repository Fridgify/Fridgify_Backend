"""Utilities for handling tokens"""
# pylint: disable=no-member

import secrets

import jwt
from django.utils import timezone
from rest_framework.exceptions import NotFound

from fridgify_backend.models import Accesstokens, Providers


def create_token(user, provider):
    """Create a token for a specific provider"""
    def generate_login(user_instance):
        """Generate a login token"""
        secret = secrets.token_hex(8)
        login_token = jwt.encode(
            payload={"user": user_instance.username, "secret": secret},
            key=secret,
            algorithm="HS256"
        ).decode("utf-8")
        return {
            "token": login_token,
            "valid_till": timezone.now() + timezone.timedelta(days=14),
            "client_id": user_instance.username,
            "client_secret": secret,
        }

    def generate():
        """Generate a generic token"""
        return {
            "token": secrets.token_hex(32),
            "valid_till": timezone.now() + timezone.timedelta(hours=1),
            "client_id": None,
            "client_secret": None,
        }

    clean_tokens(user)
    token_data = generate_login(user) if provider == "Fridgify" else generate()
    try:
        token_obj, _ = Accesstokens.objects.get_or_create(
            user=user,
            provider_id=Providers.objects.values(
                "provider_id"
            ).filter(name=provider)[0]["provider_id"],
            defaults={
                "accesstoken": token_data["token"],
                "client_id": token_data["client_id"],
                "client_secret": token_data["client_secret"],
                "valid_till": token_data["valid_till"],
            }
        )
    except IndexError:
        raise NotFound(detail="Provider does not exist")
    return token_obj.accesstoken


def clean_tokens(user):
    """Remove all expired tokens"""
    Accesstokens.objects.filter(user=user, valid_till__lte=timezone.now()).delete()
