from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Notification
from .serializers import NotificationSerializer
from django.shortcuts import get_object_or_404

class NotificationListView(APIView):
    permission_classes = []  # Allow unauthenticated access for testing

    def get(self, request):
        notifications = Notification.objects.all()  # Show all notifications for testing
        serializer = NotificationSerializer(notifications, many=True)
        return Response(serializer.data)


class MarkAsReadView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, pk):
        notification = get_object_or_404(Notification, pk=pk, user=request.user)
        notification.is_read = True
        notification.save()
        return Response({"detail": "Notification marked as read"})