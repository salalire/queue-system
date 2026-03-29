from apps.queues.models import QueueEntry


def calculate_wait_time(service, position):
    # Get last 5 completed entries
    completed = QueueEntry.objects.filter(
        service=service,
        status='done',
        completed_at__isnull=False,
        started_at__isnull=False
    ).order_by('-completed_at')[:5]

    if completed.exists():
        total_time = 0
        for entry in completed:
            duration = (entry.completed_at - entry.started_at).total_seconds() / 60
            total_time += duration

        avg_time = total_time / len(completed)
    else:
        avg_time = service.avg_service_time

    return int(position * avg_time)