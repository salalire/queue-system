from django.db import models
from django.conf import settings
from apps.services.models import Service
from core.models import TimeStampedModel

User = settings.AUTH_USER_MODEL


class QueueEntry(TimeStampedModel):

    STATUS_CHOICES = [
        ('waiting', 'Waiting'),
        ('serving', 'Serving'),
        ('done', 'Done'),
        ('skipped', 'Skipped'),
        ('cancelled', 'Cancelled'),
        ('called', 'CALLED')
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)

    position = models.PositiveIntegerField()

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='waiting'
    )

    snooze_count = models.IntegerField(default=0)

    started_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.user} - {self.service} - {self.status}"

