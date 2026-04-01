from django.db.models.signals import post_save
from django.utils import timezone
from django.dispatch import receiver
from django.db.models import Count, Avg, Q
from apps.queues.models import QueueEntry
from .models import ServiceAnalytics

@receiver(post_save, sender=QueueEntry)
def update_analysis(sender, instance, created, **kwargs):
    service = instance.service
    today = timezone.now().date()
    analytics, _ = ServiceAnalytics.objects.get_or_create(
        service = service,
        date = today
    )
    stats = QueueEntry.objects.filter(
        service = service,
        created_at__date = today
    ).aggregate(
        joined = Count('id'),
        served = Count('id', filter=Q(status='served')),
        cancelled = Count('id', filter=Q(status='cancelled')),
        avg_wait = Avg('wait_time', filter = Q(status='served'))
    )
    analytics.total_joined = stats['joined'] or 0
    analytics.total_served = stats['served'] or 0
    analytics.total_cancelled = stats['cancelled'] or 0
    analytics.avg_wait_time = stats['avg_wait'] or 0
    analytics.save()