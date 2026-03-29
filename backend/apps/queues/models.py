from django.db import models
from django.conf import settings
from apps.services.models import Service

User = settings.AUTH_USER_MODEL


class QueueEntry(models.Model):

    STATUS_CHOICES = [
        ('waiting', 'Waiting'),
        ('serving', 'Serving'),
        ('done', 'Done'),
        ('skipped', 'Skipped'),
        ('cancelled', 'Cancelled'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)

    position = models.IntegerField()

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='waiting'
    )

    joined_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # For snooze feature
    snooze_count = models.IntegerField(default=0)

    # For analytics
    started_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.user} - {self.service} - {self.status}"

# Create your models here.
