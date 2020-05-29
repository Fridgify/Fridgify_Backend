"""
Model representation for Stores
"""

from django.db import models
from rest_framework import serializers


class Stores(models.Model):
    """
    Stores a store, e.g. Rewe or Penny
    """
    store_id = models.AutoField(primary_key=True, unique=True)
    name = models.TextField(unique=True)

    def __dir__(self):
        return ["store_id", "name"]


class StoresSerializer(serializers.ModelSerializer):
    """
    Serialize Stores
    """
    class Meta:
        # pylint: disable=too-few-public-methods, missing-class-docstring
        model = Stores
        fields = "__all__"
