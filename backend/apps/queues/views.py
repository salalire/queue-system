from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.db import models
from .models import QueueEntry
from .serializer import JoinQueueSerializer
from core.utils import calculate_wait_time
from core.permissions import IsAdminUser
from django.utils import timezone


class JoinQueueView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = JoinQueueSerializer(
            data=request.data,
            context={'request': request}
        )

        if serializer.is_valid():
            queue_entry = serializer.save()
            wait_time = calculate_wait_time(queue_entry.service, queue_entry.position)

            return Response({
                "message": "Joined queue successfully",
                "queue_id": queue_entry.id,
                "position": queue_entry.position,
                "estimated_wait_time": wait_time,
                "status": queue_entry.status
            }, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MyQueueStatusView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        queue_entry = QueueEntry.objects.filter(
            user=request.user,
            status__in=['waiting', 'serving']
        ).order_by('joined_at').first()

        if not queue_entry:
            return Response({"message": "No active queue"}, status=status.HTTP_404_NOT_FOUND)

        # Fix issue 5: calculate real-time position instead of stale stored value
        real_position = QueueEntry.objects.filter(
            service=queue_entry.service,
            status='waiting',
            joined_at__lte=queue_entry.joined_at
        ).count()

        wait_time = calculate_wait_time(queue_entry.service, real_position)

        return Response({
            "queue_id": queue_entry.id,
            "service": queue_entry.service.name,
            "position": real_position,
            "status": queue_entry.status,
            "estimated_wait_time": wait_time
        })


class LeaveQueueView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        queue_entry = QueueEntry.objects.filter(
            user=request.user,
            status__in=['waiting', 'serving']
        ).order_by('joined_at').first()

        if not queue_entry:
            return Response({"message": "No active queue to leave"}, status=status.HTTP_404_NOT_FOUND)

        cancelled_position = queue_entry.position
        cancelled_service = queue_entry.service

        queue_entry.status = 'cancelled'
        queue_entry.save()

        # Fix issue 2: shift positions of everyone behind the cancelled user
        QueueEntry.objects.filter(
            service=cancelled_service,
            status='waiting',
            position__gt=cancelled_position
        ).update(position=models.F('position') - 1)

        return Response({"message": "You have left the queue successfully"}, status=status.HTTP_200_OK)


class ServeNextView(APIView):
    # Fix issue 4: only admin/staff can call this
    permission_classes = [IsAuthenticated, IsAdminUser]

    def post(self, request):
        # Fix issue 3: filter by service_id from request
        service_id = request.data.get('service_id')
        if not service_id:
            return Response({"message": "service_id is required"}, status=status.HTTP_400_BAD_REQUEST)

        current_serving = QueueEntry.objects.filter(
            service_id=service_id,
            status='serving'
        ).first()

        if current_serving:
            current_serving.status = 'done'
            current_serving.completed_at = timezone.now()
            current_serving.save()

        next_user = QueueEntry.objects.filter(
            service_id=service_id,
            status='waiting'
        ).order_by('position').first()

        if not next_user:
            return Response({"message": "No users in queue"}, status=status.HTTP_404_NOT_FOUND)

        next_user.status = 'serving'
        next_user.started_at = timezone.now()
        next_user.save()

        return Response({
            "message": "Next user is now being served",
            "queue_id": next_user.id,
            "user": str(next_user.user),
            "service": next_user.service.name,
            "position": next_user.position,
            "status": next_user.status
        }, status=status.HTTP_200_OK)
