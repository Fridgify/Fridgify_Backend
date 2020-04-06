from django.db import models
from rest_framework import serializers


class FridgeContent(models.Model):
    """
    Stores :model:`item.Items` of a :model:`fridge.Fridges`
    """
    id = models.AutoField(primary_key=True)
    fridge = models.ForeignKey('Fridges', on_delete=models.CASCADE)
    item = models.ForeignKey('Items', on_delete=models.CASCADE)
    amount = models.IntegerField()
    expiration_date = models.DateTimeField()
    unit = models.CharField(max_length=25)
    created_at = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('fridge', 'item',)

    def __dir__(self):
        return [
            "id", "fridge", "item", "amount", "expiration_date", "unit", "created_at", "last_updated"
        ]


class FridgeContentSerializer(serializers.ModelSerializer):
    expiration_date = serializers.DateTimeField(format="%Y-%m-%d")

    class Meta:
        model = FridgeContent
        fields = '__all__'
