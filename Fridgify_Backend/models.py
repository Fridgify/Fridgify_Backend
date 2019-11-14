from django.db import models


class Users(models.Model):
    user_id = models.AutoField(primary_key=True, )
    username = models.TextField(unique=True, )
    name = models.TextField()
    surname = models.TextField()
    email = models.TextField()
    password = models.CharField(max_length=60, )
    birth_date = models.DateField()
    createdAt = models.DateTimeField(auto_now_add=True)
    lastUpdatedAt = models.DateTimeField(auto_now=True)


class Providers(models.Model):
    provider_id = models.AutoField(primary_key=True, )
    name = models.CharField(max_length=255, )


# Need to think about primary keys. Just one possible. Maybe add an id?
class Accesstokens(models.Model):
    accesstoken = models.TextField()
    user_id = models.ForeignKey(Users, )
