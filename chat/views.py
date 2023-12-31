from django.http import JsonResponse, HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view
from users.utils import  login_required
from .models import Message
from .serializers import MessageSerializer
from users.models import Users
from django.db.models import Q
from .utils import add_unread_message_to_receiver


@api_view(['GET', 'DELETE'])
@login_required(RETURN_USER=True)
def message(request, user, message_id: int) -> JsonResponse:
    """
    Get or delete a specific message by its ID.

    Parameters:
        - request (HttpRequest): The HTTP request object.
        - user (Users): The authenticated user object.
        - message_id (int): The ID of the message to retrieve or delete.

    Permissions:
        - Requires the user to be the sender or the receiver.
        - Requires the user to be the sender or receiver of the message.

    Returns:
        - JsonResponse or HttpResponse: JSON response containing the serialized message object for GET request.
                                        HTTP response indicating the successful deletion for DELETE request.
    """
    message = get_object_or_404(Message, id=message_id)

    if message.sender.id != user.id and message.receiver.id != user.id:
        return HttpResponse("Uauthorized user", status=status.HTTP_401_UNAUTHORIZED)
    
    if request.method == "GET":

        message_serializer = MessageSerializer(message)
        return JsonResponse(message_serializer.data)
    
    if request.method == "DELETE":

        message.delete()
        return HttpResponse("successfully deleted message", status=status.HTTP_204_NO_CONTENT)
    
 
@api_view(['POST'])
@login_required(RETURN_USER=True)
def post_new_message(request, user) -> JsonResponse:
    """
    Create a new message.
    
    Permissions:
        - No specific user authentication required.
    
    Returns:
        - JsonResponse: JSON response containing the serialized message object and ID.
    """
    message_serializer = MessageSerializer(data=request.data, context={'user': user, 'request': request})
    if message_serializer.is_valid():
        message_serializer.save()
        

        receiver_user = message_serializer.validated_data['receiver']
        message_id = message_serializer.data['id']

        add_unread_message_to_receiver(receiver_user, message_id)   
            
        return JsonResponse(message_serializer.data, status=status.HTTP_201_CREATED)

    return HttpResponse(message_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@login_required(RETURN_USER=True)
def get_all_user_unread_messages(request, user: Users) -> JsonResponse:
    """
    Retrieve all unread messages for a specific user.
    
    Parameters:
        - user_id (int): The ID of the user.
    
    Permissions:
        - Requires the user to be authenticated.
    
    Returns:
        - JsonResponse: JSON response containing the serialized unread message objects.
    """
    unread_messages = user.unreadMessages.all()

    serializer = MessageSerializer(unread_messages, many=True)

    all_unread_message_seri = serializer.data

    user.unreadMessages.clear()

    return JsonResponse(all_unread_message_seri, safe=False)

@api_view(['GET'])
@login_required(RETURN_USER=True)
def get_all_user_messages(request, user: Users) -> JsonResponse:
    """
    Retrieve all messages (both sent and received) for a specific user.
    
    Parameters:
        - user_id (int): The ID of the user.
    
    Permissions:
        - Requires the user to be authenticated.
    
    Returns:
        - JsonResponse: JSON response containing the serialized message objects.
    """
    messages = Message.objects.filter(Q(sender=user) | Q(receiver=user))
    serializer = MessageSerializer(messages, many=True) # Retrieve the user

    user.unreadMessages.clear()

    return JsonResponse(serializer.data, safe=False)
    
