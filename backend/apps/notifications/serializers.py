from rest_framework import serializers
from .models import Notification

class NotificationSerializer(serializers.ModelSerializer):
    user_name = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Notification
        fields = ['user', 'user_name', 'ticket', 'recipient_number', 'message_body', 'status', 'provider_message_id', 'error_message']
        read_only_fields = ['id', 'status', 'provider_message_id', 'error_message', 'created_at', 'sent_at']