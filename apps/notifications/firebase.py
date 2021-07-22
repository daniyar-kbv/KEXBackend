# Copyright 2018 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import print_function
from config.settings import Languages

import datetime
import logging

from django.conf import settings
from firebase_admin import messaging, credentials, initialize_app
cred = credentials.Certificate(settings.GOOGLE_APPLICATION_CREDENTIALS)
# cred = credentials.Certificate("/home/sultan/mentalmind-back/google-credentials.json")
# cred = credentials.Certificate("/Users/Asus/PycharmProjects/customusers/django_auth/google-credentials.json")
initialize_app(cred)

logger = logging.getLogger('fcm')


def fcm_send_to_token():
    # [START send_to_token]
    # This registration token comes from the client FCM SDKs.
    registration_token = 'YOUR_REGISTRATION_TOKEN'

    # See documentation on defining a message payload.
    message = messaging.Message(
        data={
            'score': '850',
            'time': '2:45',
        },
        token=registration_token,
    )

    # Send a message to the device corresponding to the provided
    # registration token.
    response = messaging.send(message)
    # Response is a message ID string.
    print('Successfully sent message:', response)
    # [END send_to_token]


def send_to_token(fb_token, title, body, extra={}):
    message = messaging.Message(
        notification=messaging.Notification(
            title=str(title),
            body=str(body),
        ),
        token=fb_token,
        data=extra
    )
    response = messaging.send(message)
    print('Sent message:', response)


def fcm_send_to_topic():
    # [START send_to_topic]
    # The topic name can be optionally prefixed with "/topics/".
    topic = 'highScores'

    # See documentation on defining a message payload.
    message = messaging.Message(
        notification=messaging.Notification(
            title='$GOOG up 1.43% on the day',
            body='$GOOG gained 11.80 points to close at 835.67, up 1.43% on the day.',
        ),
        topic=topic,
    )

    # Send a message to the devices subscribed to the provided topic.
    response = messaging.send(message)
    # Response is a message ID string.
    print('Successfully sent message:', response)
    # [END send_to_topic]


def fcm_send_to_condition():
    # [START send_to_condition]
    # Define a condition which will send to devices which are subscribed
    # to either the Google stock or the tech industry topics.
    condition = "'stock-GOOG' in topics || 'industry-tech' in topics"

    # See documentation on defining a message payload.
    message = messaging.Message(
        notification=messaging.Notification(
            title='$GOOG up 1.43% on the day',
            body='$GOOG gained 11.80 points to close at 835.67, up 1.43% on the day.',
        ),
        condition=condition,
    )

    # Send a message to devices subscribed to the combination of topics
    # specified by the provided condition.
    response = messaging.send(message)
    # Response is a message ID string.
    print('Successfully sent message:', response)
    # [END send_to_condition]


def fcm_send_dry_run():
    message = messaging.Message(
        data={
            'score': '850',
            'time': '2:45',
        },
        token='token',
    )

    # [START send_dry_run]
    # Send a message in the dry run mode.
    response = messaging.send(message, dry_run=True)
    # Response is a message ID string.
    print('Dry run successful:', response)
    # [END send_dry_run]


def fcm_android_message():
    # [START android_message]
    message = messaging.Message(
        android=messaging.AndroidConfig(
            ttl=datetime.timedelta(seconds=3600),
            priority='normal',
            notification=messaging.AndroidNotification(
                title='$GOOG up 1.43% on the day',
                body='$GOOG gained 11.80 points to close at 835.67, up 1.43% on the day.',
                icon='stock_ticker_update',
                color='#f45342'
            ),
        ),
        topic='industry-tech',
    )
    # [END android_message]
    return message


def fcm_apns_message():
    # [START apns_message]
    message = messaging.Message(
        apns=messaging.APNSConfig(
            headers={'apns-priority': '10'},
            payload=messaging.APNSPayload(
                aps=messaging.Aps(
                    alert=messaging.ApsAlert(
                        title='$GOOG up 1.43% on the day',
                        body='$GOOG gained 11.80 points to close at 835.67, up 1.43% on the day.',
                    ),
                    badge=42,
                ),
            ),
        ),
        topic='industry-tech',
    )
    # [END apns_message]
    return message


def fcm_webpush_message():
    # [START webpush_message]
    message = messaging.Message(
        webpush=messaging.WebpushConfig(
            notification=messaging.WebpushNotification(
                title='$GOOG up 1.43% on the day',
                body='$GOOG gained 11.80 points to close at 835.67, up 1.43% on the day.',
                icon='https://my-server/icon.png',
            ),
        ),
        topic='industry-tech',
    )
    # [END webpush_message]
    return message


def fcm_all_platforms_message():
    # [START multi_platforms_message]
    message = messaging.Message(
        notification=messaging.Notification(
            title='$GOOG up 1.43% on the day',
            body='$GOOG gained 11.80 points to close at 835.67, up 1.43% on the day.',
        ),
        android=messaging.AndroidConfig(
            ttl=datetime.timedelta(seconds=3600),
            priority='normal',
            notification=messaging.AndroidNotification(
                icon='stock_ticker_update',
                color='#f45342'
            ),
        ),
        apns=messaging.APNSConfig(
            payload=messaging.APNSPayload(
                aps=messaging.Aps(badge=42),
            ),
        ),
        topic='industry-tech',
    )
    # [END multi_platforms_message]
    return message


def fcm_subscribe_to_topic():
    topic = 'highScores'
    # [START subscribe]
    # These registration tokens come from the client FCM SDKs.
    registration_tokens = [
        'YOUR_REGISTRATION_TOKEN_1',
        # ...
        'YOUR_REGISTRATION_TOKEN_n',
    ]

    # Subscribe the devices corresponding to the registration tokens to the
    # topic.
    response = messaging.subscribe_to_topic(registration_tokens, topic)
    # See the TopicManagementResponse reference documentation
    # for the contents of response.
    print(response.success_count, 'tokens were subscribed successfully')
    # [END subscribe]


def subscribe_to_topic(topic, registration_tokens=[]):
    # no more than 1000 elements in registration_tokens

    if isinstance(registration_tokens, str):
        registration_tokens = [registration_tokens]
    response = messaging.subscribe_to_topic(registration_tokens, topic)
    print(response.errors)
    print(response.success_count, ' tokens were subscribed successfully')
    print(response.failure_count, ' failed')


def subscribe_to_language_topic(topic, registration_tokens=[]):
    # no more than 1000 elements in registration_tokens
    print("subscribe_to_language_topic started")
    langs = [str(l) for l in Languages]
    if isinstance(registration_tokens, str):
        registration_tokens = [registration_tokens]
    response = messaging.subscribe_to_topic(registration_tokens, topic)
    print(response.success_count, ' tokens were subscribed successfully')
    print(response.failure_count, ' failed')
    if response.failure_count > 0:
        print(response.errors[0])
        print(response.errors[0].__dict__)
    langs.remove(topic)
    for lang in langs:
        unsubscribe_from_topic(lang, registration_tokens)

    print("subscribe_to_language_topic ended")


def unsubscribe_from_topic(topic, registration_tokens=[]):
    # no more than 1000 elements in registration_tokens

    if isinstance(registration_tokens, str):
        registration_tokens = [registration_tokens]
    response = messaging.unsubscribe_from_topic(registration_tokens, topic)
    print(response.errors)
    print(response.success_count, ' tokens were unsubscribed successfully')
    print(response.failure_count, ' failed')


if __name__ == '__main__':
    tokens = [
        # "eiq4H_1gRsC-Y31L3u4XUx:APA91bFau_Gj18VkLZI8le2V4GwjFe5DvZHItcZWtab_tsWlaWSFujFTEhjmQRbnsGTz8QMo0B-LCdwwCuDj6-Hl0RkCcraiCf9ddBqBDqBhVtOiQ9b1h06lOjM28jGMwmFjmU1jFtTJ",
        "eEo_X58wR0KMBxs3Oy-Bbs:APA91bG-n9hAmuEvWxHmOE34iX2PNVRTAAXyKbPYh1pVFQeqTjh1MJ9XZWyPijDgq02KoLa6AmQiuo0KWQBSvVRdlK9NV9Ydu47XOppkSTrPYsnsq8nLrv_8yaBUvB_H6sraGpYraOHY",
    ]
    subscribe_to_topic(Languages.RUSSIAN, tokens)
    unsubscribe_from_topic(Languages.KAZAKH, tokens)
    unsubscribe_from_topic(Languages.ENGLISH, tokens)


def fcm_unsubscribe_from_topic():
    topic = 'highScores'
    # [START unsubscribe]
    # These registration tokens come from the client FCM SDKs.
    registration_tokens = [
        'YOUR_REGISTRATION_TOKEN_1',
        # ...
        'YOUR_REGISTRATION_TOKEN_n',
    ]

    # Unubscribe the devices corresponding to the registration tokens from the
    # topic.
    response = messaging.unsubscribe_from_topic(registration_tokens, topic)
    # See the TopicManagementResponse reference documentation
    # for the contents of response.
    print(response.success_count, 'tokens were unsubscribed successfully')
    # [END unsubscribe]


def fcm_send_all():
    registration_token = 'YOUR_REGISTRATION_TOKEN'
    # [START send_all]
    # Create a list containing up to 500 messages.
    messages = [
        messaging.Message(
            notification=messaging.Notification('Price drop', '5% off all electronics'),
            token=registration_token,
        ),
        # ...
        messaging.Message(
            notification=messaging.Notification('Price drop', '2% off all books'),
            topic='readers-club',
        ),
    ]

    response = messaging.send_all(messages)
    # See the BatchResponse reference documentation
    # for the contents of response.
    print('{0} messages were sent successfully'.format(response.success_count))
    # [END send_all]


def push_broadcast(notify_data):
    print("FCM: push_broadcast started")
    messages = [
        messaging.Message(
            notification=messaging.Notification(
                title=notify_data[ lang[0] ]['title'],
                body=notify_data[ lang[0] ]['body'],
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


def fcm_send_multicast():
    # [START send_multicast]
    # Create a list containing up to 500 registration tokens.
    # These registration tokens come from the client FCM SDKs.
    registration_tokens = [
        'YOUR_REGISTRATION_TOKEN_1',
        # ...
        'YOUR_REGISTRATION_TOKEN_N',
    ]

    message = messaging.MulticastMessage(
        data={'score': '850', 'time': '2:45'},
        tokens=registration_tokens,
    )
    response = messaging.send_multicast(message)
    # See the BatchResponse reference documentation
    # for the contents of response.
    print('{0} messages were sent successfully'.format(response.success_count))
    # [END send_multicast]


def push_multicast(user_tokens, notify_data, extra_data=None):
    # Create a list containing up to 500 registration tokens.
    if not isinstance(user_tokens, list):
        user_tokens = [user_tokens]
    message = messaging.MulticastMessage(
        notification=messaging.Notification(**notify_data),
        data=extra_data,
        tokens=user_tokens,
    )
    response = messaging.send_multicast(message)
    print('{0} messages were sent successfully'.format(response.success_count))


def push_multicast_by_language(users):
    messages = []
    for obj in users:
        messages.append(messaging.Message(
            notification=messaging.Notification(
                title=obj['title'],
                body=obj['body'],
            ),
            token=obj['token'],
            data=obj.get('extra_data')
        ))

    response = messaging.send_all(messages)
    print("FCM: push_multicast_by_language finished")
    print(response.responses)
    print('{0}/{1} messages were sent successfully'.format(response.success_count, len(messages)))


def fcm_send_multicast_and_handle_errors():
    # [START send_multicast_error]
    # These registration tokens come from the client FCM SDKs.
    registration_tokens = [
        'YOUR_REGISTRATION_TOKEN_1',
        # ...
        'YOUR_REGISTRATION_TOKEN_N',
    ]

    message = messaging.MulticastMessage(
        data={'score': '850', 'time': '2:45'},
        tokens=registration_tokens,
    )
    response = messaging.send_multicast(message)
    print('{0} messages were sent successfully'.format(response.success_count))

    if response.failure_count > 0:
        responses = response.responses
        failed_tokens = []
        for idx, resp in enumerate(responses):
            if not resp.success:
                # The order of responses corresponds to the order of the registration tokens.
                failed_tokens.append(registration_tokens[idx])
        print('List of tokens that caused failures: {0}'.format(failed_tokens))
    # [END send_multicast_error]
