from firebase_admin import messaging

from Fridgify_Backend.utils.messaging import auth


def send_message(tokens, title, content, fridge_id=0):
    auth.FirebaseMessaging.get_instance()

    message = messaging.MulticastMessage(
        tokens=tokens,
        data={"fridge_id": str(fridge_id)},
        notification=messaging.Notification(
            title=title,
            body=content
        )
    )

    response = messaging.send_multicast(message)
    print('Successfully sent message:', response)
