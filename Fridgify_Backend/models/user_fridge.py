from django.db import models


class UserFridge(models.Model):
    """
    Stores all :model:`fridge.Fridges` of a :model:'user.Users'
    """
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey('Users', on_delete=models.CASCADE)
    fridge = models.ForeignKey('Fridges', on_delete=models.CASCADE)

    def __dir__(self):
        return ["id", "user", "fridge"]