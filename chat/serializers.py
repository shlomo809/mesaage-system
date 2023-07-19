from rest_framework import serializers
from .models import Message
from users.serializers import UsersSerializer



class MessageSerializer(serializers.ModelSerializer):


    class Meta:
        model = Message
        fields = ['id', 'message', 'subject', 'sender', 'receiver', 'date']


    def validate(self, data):
        sender = data.get('sender')
        receiver = data.get('receiver')
        # Check if the sender and receiver are the same
        if sender.id == receiver.id:
            raise serializers.ValidationError("Sender and receiver cannot be the same.")
        
        user = self.context.get('user')

        if user.id != sender.id:
            raise serializers.ValidationError("Authenticated user is not the sender.")
        return data
