from django.db import models
from apps.services.models import Service


class ServiceAnalytics(models.Model):
    """Stores daily aggregated analytics per service."""
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='analytics')
    date = models.DateField()

    total_joined = models.IntegerField(default=0)      # how many joined
    total_served = models.IntegerField(default=0)      # how many completed
    total_cancelled = models.IntegerField(default=0)   # how many left/cancelled
    avg_wait_time = models.FloatField(default=0.0)     # average wait in minutes

    class Meta:
        unique_together = ('service', 'date')          # one record per service per day

    def __str__(self):
        return f"{self.service.name} - {self.date}"
