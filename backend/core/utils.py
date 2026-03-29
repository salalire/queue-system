from apps.queues.models import QueueEntry


def calculate_wait_time(service, position):
    # Get last 5 completed entries
    completed = QueueEntry.objects.filter(
        service=service,
        status='done',
        completed_at__isnull=False,
        started_at__isnull=False
    ).order_by('-completed_at')[:5]

    completed_list = list(completed)

    if completed_list:
        total_time = sum(
            (entry.completed_at - entry.started_at).total_seconds() / 60
            for entry in completed_list
        )
        avg_time = total_time / len(completed_list)
    else:
        avg_time = service.avg_service_time

    # fallback if avg_time ended up as 0 (e.g. bad historical data)
    if avg_time == 0:
        avg_time = service.avg_service_time

    return int(position * avg_time)