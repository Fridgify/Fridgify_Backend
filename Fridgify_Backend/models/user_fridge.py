from django.db import models


class UserFridge(models.Model):
    """
    Stores all :model:`fridge.Fridges` of a :model:'user.Users'
    """
    OWNER = 0
    OVERSEER = 1
    USER = 2

    ROLES = [(OWNER, "Fridge Owner"), (OVERSEER, "Fridge Overseer"), (USER, "Fridge User")]

    id = models.AutoField(primary_key=True)
    user = models.ForeignKey('Users', on_delete=models.CASCADE)
    fridge = models.ForeignKey('Fridges', on_delete=models.CASCADE)
    role = models.IntegerField(choices=ROLES, default=USER)

    choices = [
        (0, "Fridge Owner"),
        (1, "Fridge Overseer"),
        (2, "Fridge User")
    ]

    def __dir__(self):
        return ["id", "user", "fridge", "role"]