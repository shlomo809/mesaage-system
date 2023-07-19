from django.urls import path

from . import views
urlpatterns = [
    path('user/<int:user_id>/chat/post-new-message', views.post_new_message, name='post_new_message'),
    path('user/<int:user_id>/chat/get-all-user-messages', views.get_all_user_messages, name='get_all_user_messages'),
    path('user/<int:user_id>/chat/get-all-user-unread-messages', views.get_all_user_unread_messages, name='get_all_user_unread_messages'),
    path('user/<int:user_id>/chat/<int:message_id>', views.message, name='message'),
] 