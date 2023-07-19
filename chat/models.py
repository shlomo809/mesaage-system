from django.db import models


# Create your models here.
class Message(models.Model):
    message  = models.TextField()
    subject  = models.CharField(max_length=300)
    date = models.DateTimeField(auto_now=True)
    sender = models.ForeignKey('users.Users', on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey('users.Users', on_delete=models.CASCADE, related_name='received_messages')