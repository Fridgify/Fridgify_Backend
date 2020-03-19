from django.db import models


class Accesstokens(models.Model):
    token_id = models.AutoField(primary_key=True, unique=True)
    accesstoken = models.TextField()
    client_id = models.TextField(null=True)
    client_secret = models.TextField(null=True)
    provider = models.ForeignKey("Providers", on_delete=models.CASCADE)
    valid_till = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey('Users', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('provider', 'user',)

    def __dir__(self):
        return [
            "token_id",
            "accesstoken",
            "client_id",
            "client_secret",
            "provider",
            "valid_till",
            "created_at",
            "updated_at",
            "user"
        ]