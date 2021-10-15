from typing import List

from django.conf import settings
from firebase_admin import messaging, credentials, initialize_app

from config.settings import Languages

cred = credentials.Certificate(settings.GOOGLE_APPLICATION_CREDENTIALS)
initialize_app(cred)


def subscribe_to_topic(topic: str, registration_tokens: List[str]) -> None:
    print(f'SUBSCRIBE_TO_TOPIC. {len(registration_tokens)} device to {topic}')
    messaging.subscribe_to_topic(registration_tokens, topic)


def unsubscribe_from_topic(topic: str, registration_tokens: List[str]) -> None:
    print(f'UNSUBSCRIBE_TO_TOPIC. {len(registration_tokens)} device from {topic}')
    messaging.unsubscribe_from_topic(registration_tokens, topic)


def push_broadcast(notify_data):
    print("FCM: push_broadcast started")
    messages = [
        messaging.Message(
            notification=messaging.Notification(
                title=notify_data[lang[0]]['title'],
                body=notify_data[lang[0]]['body'],
            ),
            topic=lang[0],
            data=notify_data['extra']
        ) for lang in Languages.choices
    ]

    response = messaging.send_all(messages)
    print(response.responses)
    if response.failure_count > 0:
        print(response.failure_count)
        print(response.responses[0].__dict__)
    print('{0} messages were sent successfully'.format(response.success_count))
    print("FCM: push_broadcast finished")


def push_multicast(user_tokens, title, body, extra_data=None):
    # Create a list containing up to 500 registration tokens.
    if not isinstance(user_tokens, list):
        user_tokens = [user_tokens]
    message = messaging.MulticastMessage(
        notification=messaging.Notification(
            title=str(title),
            body=str(body)
        ),
        data=extra_data,
        tokens=user_tokens,
    )
    response = messaging.send_multicast(message)
    print('{0} messages were sent successfully'.format(response.success_count))
