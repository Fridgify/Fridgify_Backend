"""Fridgify Constants"""


class Constants:
    #  pylint: disable=too-few-public-methods
    """Contains all constants"""
    ROLE_OWNER = 0
    ROLE_OVERSEER = 1
    ROLE_USER = 2
    ROLES = [ROLE_OWNER, ROLE_OVERSEER, ROLE_USER]

    ROLE_S_OWNER = "Fridge Owner"
    ROLE_S_OVERSEER = "Fridge Overseer"
    ROLE_S_USER = "Fridge User"
    ROLES_S = [ROLE_S_OWNER, ROLE_S_OVERSEER, ROLE_S_USER]

    ROLE_CHOICES = list(zip(ROLES, ROLES_S))

    FRY_NOTIFICATION_SERVICE = 4  # Fridgify Notification Service
    HP_NOTIFICATION_SERVICE = 5  # Hopper Notification Service
    NOTIFICATION_SERVICES = [
        FRY_NOTIFICATION_SERVICE,
        HP_NOTIFICATION_SERVICE
    ]
    NOTIFICATION_SERVICES_DICT = {
        1: FRY_NOTIFICATION_SERVICE,
        2: HP_NOTIFICATION_SERVICE
    }
