from django.db import models
from django.conf import settings
from core.models import TimeStampedModel

class Notification(TimeStampedModel):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='notifications'
    )
    ticket = models.ForeignKey(
        'queues.QueueEntry', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True
    )

    recipient_number = models.CharField(max_length=20) 
    message_body = models.TextField()
    
    provider_message_id = models.CharField(max_length=255, unique=True, null=True, blank=True)
    provider_name = models.CharField(max_length=50, default='INFOBIP') 

    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('SENT', 'Sent'),
        ('DELIVERED', 'Delivered'),
        ('FAILED', 'Failed'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    error_message = models.TextField(null=True, blank=True) 
    sent_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Notification to {self.user.username} - {self.status}"