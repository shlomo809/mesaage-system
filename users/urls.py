from django.urls import path

from . import views

urlpatterns = [
   path("user/create_new_user", views.create_new_user),
   path("user/<int:user_id>/login", views.update_login_status, {'is_logged_in': True}),
   path("user/<int:user_id>/logout", views.update_login_status, {'is_logged_in': False}),

]