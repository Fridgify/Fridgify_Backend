"""
Model representation for UserFridge
"""

from django.db import models
from rest_framework import serializers

from fridgify_backend.models import UserSerializer
from fridgify_backend.utils import const


class UserFridge(models.Model):
    """
    Stores all :model:`fridge.Fridges` of a :model:'user.Users'
    """
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey('Users', on_delete=models.CASCADE)
    fridge = models.ForeignKey('Fridges', on_delete=models.CASCADE)
    role = models.IntegerField(
        choices=const.Constants.ROLE_CHOICES,
        default=const.Constants.ROLE_USER
    )

    class Meta:
        # pylint: disable=too-few-public-methods, missing-class-docstring
        unique_together = ('user', 'fridge',)


class FridgeUserSerializer(serializers.ModelSerializer):
    """
    Serialize FridgeUser
    """
    user = UserSerializer()

    class Meta:
        # pylint: disable=too-few-public-methods, missing-class-docstring
        model = UserFridge
        fields = ["user", "role"]

    def to_representation(self, instance: UserFridge):
        if instance.role == const.Constants.ROLE_OWNER:
            instance.role = const.Constants.ROLE_S_OWNER
        elif instance.role == const.Constants.ROLE_OVERSEER:
            instance.role = const.Constants.ROLE_S_OVERSEER
        else:
            instance.role = const.Constants.ROLE_S_USER
        return super().to_representation(instance)
