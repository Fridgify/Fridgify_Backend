import firebase_admin


class FirebaseMessaging:
    __instance = None

    @staticmethod
    def get_instance():
        if FirebaseMessaging.__instance is None:
            FirebaseMessaging()

    def __init__(self):
        if FirebaseMessaging.__instance is not None:
            raise Exception("This class is a singleton")
        else:
            self.app = firebase_admin.initialize_app()
            FirebaseMessaging.__instance = self
