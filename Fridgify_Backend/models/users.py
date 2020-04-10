from django.db import models
from rest_framework import serializers


class Users(models.Model):
    """
    Stores a user
    """
    user_id = models.AutoField(primary_key=True, unique=True)
    username = models.TextField(unique=True)
    name = models.TextField()
    surname = models.TextField()
    email = models.TextField(unique=True)
    password = models.CharField(max_length=60, )
    birth_date = models.DateField()
    createdAt = models.DateTimeField(auto_now_add=True)
    lastUpdatedAt = models.DateTimeField(auto_now=True)
    is_authenticated = False
    token_authentication = None

    def __dir__(self):
        return [
            "user_id",
            "username",
            "name",
            "surname",
            "email",
            "password",
            "birth_date",
            "createdAt",
            "lastUpdatedAt",
            "is_authenticated",
            "token_authentication"
        ]


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ["username", "password", "name", "surname", "email", "birth_date"]
