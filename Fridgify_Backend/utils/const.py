from Fridgify_Backend import models


class Constants:
    ROLE_OWNER = 0
    ROLE_OVERSEER = 1
    ROLE_USER = 2
    ROLES = [ROLE_OWNER, ROLE_OVERSEER, ROLE_USER]

    ROLE_S_OWNER = "Fridge Owner"
    ROLE_S_OVERSEER = "Fridge Overseer"
    ROLE_S_USER = "Fridge User"
    ROLES_S = [ROLE_S_OWNER, ROLE_S_OVERSEER, ROLE_S_USER]

    ROLE_CHOICES = list(zip(ROLES, ROLES_S))

    FRY_NOTIFICATION_SERVICE = 4
    NOTIFICATION_SERVICES = [
        FRY_NOTIFICATION_SERVICE
    ]
