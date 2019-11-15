from django.db import models


class Accesstokens(models.Model):
    token_id = models.AutoField(primary_key=True, unique=True)
    accesstoken = models.TextField()
    provider_id = models.ForeignKey("Providers", on_delete=models.CASCADE)
    valid_till = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user_id = models.ForeignKey('Users', on_delete=models.CASCADE)
