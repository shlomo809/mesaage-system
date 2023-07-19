from django.http import JsonResponse, HttpResponse
from django.shortcuts import get_object_or_404, render
from rest_framework.decorators import api_view
from .serializers import UsersSerializer
from rest_framework import status
from .models import Users
import secrets
# Create your views here.


@api_view(['POST'])
def create_new_user(request) -> JsonResponse:
    """
    Create a new user.

    Permissions:
        - No specific user authentication required.

    Returns:
        - JsonResponse: JSON response containing the serialized user object if successful,
          or error details if there are validation errors.
    """
    serializer = UsersSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
    return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
def update_login_status(request, user_id: int, is_logged_in: bool) -> HttpResponse:
    """
    Update the logged-in status of a user.

    Parameters:
        - user_id (int): The ID of the user.
        - is_logged_in (bool): Flag indicating whether the user should be logged in or logged out.

    Permissions:
        - No specific user authentication required.

    Returns:
        - HttpResponse: HTTP response indicating the successful login or logout.
    """
    user = get_object_or_404(Users, id=user_id)

    if is_logged_in:

        if user.isLoggedIn:
            return HttpResponse("already logged in")
        
        return login_handler(user, True, "successfully logged in")

    else:
        if not user.isLoggedIn:
            return HttpResponse("already logged out")
        
        return login_handler(user, False, "successfully logged out")

    
def login_handler(user: Users, logged_in:bool, response_message: str):

    user.isLoggedIn = logged_in
    user.save()
        
    return HttpResponse(response_message)