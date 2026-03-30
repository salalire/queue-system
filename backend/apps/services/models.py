from django.db import models
from core.models import TimeStampedModel

class Service(TimeStampedModel):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    priority_level = models.IntegerField(default=1)
    avg_service_time = models.IntegerField(help_text="Average time in minutes",default=10)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name