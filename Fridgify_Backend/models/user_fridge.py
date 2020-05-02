from django.db import models
from rest_framework import serializers

from Fridgify_Backend.models import UserSerializer
from Fridgify_Backend.utils import const


class UserFridge(models.Model):
    """
    Stores all :model:`fridge.Fridges` of a :model:'user.Users'
    """
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey('Users', on_delete=models.CASCADE)
    fridge = models.ForeignKey('Fridges', on_delete=models.CASCADE)
    role = models.IntegerField(choices=const.ROLE_CHOICES, default=const.ROLE_USER)

    def __dir__(self):
        return ["id", "user", "fridge", "role"]


class FridgeUserSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = UserFridge
        fields = ["user", "role"]

    def to_representation(self, instance:UserFridge):
        if instance.role == const.ROLE_OWNER:
            instance.role = const.ROLE_S_OWNER
        elif instance.role == const.ROLE_OVERSEER:
            instance.role = const.ROLE_S_OVERSEER
        else:
            instance.role = const.ROLE_S_USER
        return super().to_representation(instance)