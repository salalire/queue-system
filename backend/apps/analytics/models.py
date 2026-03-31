from django.db import models
from apps.services.models import Service
from core.models import TimeStampedModel


class ServiceAnalytics(TimeStampedModel):
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='analytics')
    date = models.DateField()

    total_joined = models.IntegerField(default=0)
    total_served = models.IntegerField(default=0)
    total_cancelled = models.IntegerField(default=0)   
    avg_wait_time = models.FloatField(default=0.0)
    class Meta:
        unique_together = ('service', 'date')
    def __str__(self):
        return f"{self.service.name} - {self.date}"