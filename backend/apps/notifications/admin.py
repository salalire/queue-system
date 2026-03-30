from django.contrib import admin
from .models import Notification

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'ticket', 'recipient_number', 'message_body', 'status', 'provider_message_id', 'error_message', 'created_at', 'sent_at')