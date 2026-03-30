from rest_framework import viewsets
from core.permissions import IsStaffOrOwner
from .models import Notification
from .serializers import NotificationSerializer

class UserNotificationListView(viewsets.ModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = [IsStaffOrOwner]

    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user)