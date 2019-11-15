from django.db import models


class Accesstokens(models.Model):
    token_id = models.AutoField(primary_key=True, unique=True)
    accesstoken = models.TextField()
    user_id = models.ForeignKey('Users', on_delete=models.CASCADE)
