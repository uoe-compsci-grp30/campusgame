# Set Celery tasks here
from asgiref.sync import async_to_sync
from celery import shared_task
from channels.layers import get_channel_layer

from games.consumers import MessageType


@shared_task
def send_test_messages():
    channel_layer = get_channel_layer()

    async_to_sync(channel_layer.group_send)(
        "game_2ad0744d-8de7-4e45-8a1c-6452be8cd40e",
        {
            "type": MessageType.chat_message.name,
            "message_d": {
                "type": MessageType.chat_message.name,
                "payload": "Test message sent from celery",
                "uid": ""
            }
        }
    )
