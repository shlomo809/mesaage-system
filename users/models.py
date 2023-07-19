from django.db import models

class Users(models.Model):
    username = models.CharField(max_length=150, blank=False, unique=True)    
    unreadMessages = models.ManyToManyField('chat.Message', related_name='related_users')
    isLoggedIn = models.BooleanField(default=True)
    