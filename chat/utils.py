from django.shortcuts import get_object_or_404
from .models import Message
from users.models import Users

def add_unread_message_to_receiver(receiver_user: Users, message_id: int) -> None:
    """
    Add an unread message to the receiver's unreadMessages field.

    Parameters:
        - receiver_user (Users): The user who will receive the message.
        - message_id (int): The ID of the message to be added.

    Returns:
        - None
    """

    message = get_object_or_404(Message, id=message_id)
    receiver_user.unreadMessages.add(message)
    receiver_user.save()