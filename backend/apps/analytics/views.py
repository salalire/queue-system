from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.utils import timezone
from django.db.models import Avg, Count
from apps.queues.models import QueueEntry
from apps.services.models import Service
from core.permissions import IsAdminUser


class ServiceAnalyticsView(APIView):
    """Admin: get analytics summary for a specific service."""
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get(self, request, service_id):
        try:
            service = Service.objects.get(id=service_id)
        except Service.DoesNotExist:
            return Response({"message": "Service not found"}, status=status.HTTP_404_NOT_FOUND)

        entries = QueueEntry.objects.filter(service=service)

        total_joined = entries.count()
        total_served = entries.filter(status='done').count()
        total_cancelled = entries.filter(status='cancelled').count()
        currently_waiting = entries.filter(status='waiting').count()

        # avg wait time from real completed entries
        completed = entries.filter(
            status='done',
            started_at__isnull=False,
            completed_at__isnull=False
        )
        avg_wait = 0.0
        if completed.exists():
            total_time = sum(
                (e.completed_at - e.started_at).total_seconds() / 60
                for e in completed
            )
            avg_wait = round(total_time / completed.count(), 2)

        return Response({
            "service": service.name,
            "total_joined": total_joined,
            "total_served": total_served,
            "total_cancelled": total_cancelled,
            "currently_waiting": currently_waiting,
            "avg_service_time_minutes": avg_wait
        })


class AllServicesAnalyticsView(APIView):
    """Admin: get a summary across all services."""
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get(self, request):
        services = Service.objects.filter(is_active=True)
        result = []

        for service in services:
            entries = QueueEntry.objects.filter(service=service)
            total_served = entries.filter(status='done').count()
            currently_waiting = entries.filter(status='waiting').count()

            result.append({
                "service_id": service.id,
                "service": service.name,
                "total_served": total_served,
                "currently_waiting": currently_waiting,
            })

        return Response(result)
