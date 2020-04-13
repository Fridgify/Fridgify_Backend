from django.db import models
from rest_framework import serializers


class Fridges(models.Model):
    """
    Stores all fridges
    """
    fridge_id = models.AutoField(primary_key=True, unique=True)
    name = models.TextField()
    description = models.TextField(default="")

    def __dir__(self):
        return ["fridge_id", "name", "description"]


class FridgeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fridges
        fields = '__all__'
