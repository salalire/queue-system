from rest_framework import viewsets, status
from rest_framework.response import Response
from core.permissions import IsStaffOrOwner
from .models import QueueEntry
from .serializer import JoinQueueSerializer
from core.utils import calculate_wait_time
from rest_framework.exceptions import ValidationError


class QueueViewSet(viewsets.ModelViewSet):
    queryset = QueueEntry.objects.all()
    serializer_class = JoinQueueSerializer
    permission_classes = [IsStaffOrOwner]

    def get_queryset(self):
        return QueueEntry.objects.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            queue_entry = serializer.save()

            wait_time = calculate_wait_time(
                queue_entry.service,
                queue_entry.position
            )

            return Response({
                "message": "Joined queue successfully",
                "queue_id": queue_entry.id,
                "position": queue_entry.position,
                "estimated_wait_time": wait_time,
                "status": queue_entry.status
            }, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def perform_update(self, serializer):
        instance = self.get_object()
        if instance.status != 'waiting':
            raise ValidationError(
                f"Cannot update a ticket that is already {instance.status}."
            )
        serializer.save()
    
    def perform_destroy(self, instance):
        # Check status before allowing a deletion (Cancellation)
        if instance.status != 'waiting':
            raise ValidationError(
                f"Cannot cancel a ticket that is already {instance.status}."
            )
        
        # send_sms(instance.user.phone_number, "Your queue entry has been cancelled.")
        
        instance.delete()