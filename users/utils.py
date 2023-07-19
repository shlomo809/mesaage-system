from functools import wraps
from django.http import HttpResponse, HttpResponseForbidden
from django.shortcuts import get_object_or_404
from chat.models import Message
from users.models import Users
from rest_framework import status


def login_required(RETURN_USER: bool = False):
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, user_id, *args, **kwargs):
            # Check if the Authorization header is present in the request
            user = get_object_or_404(Users, id=user_id)

            if user.isLoggedIn == False:
                return HttpResponseForbidden('User not logged in')
            
            return view_func(request, user, *args, **kwargs) if RETURN_USER else view_func(request, *args, **kwargs)
        
        return wrapper
    return decorator