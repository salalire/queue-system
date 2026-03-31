from rest_framework import viewsets
from .serializers import AnalyticsSerializer
from .models import ServiceAnalytics

class AnalyticsVewSet(viewsets.ModelViewSet):
    queryset = ServiceAnalytics.objects.all()
    serializer_class = AnalyticsSerializer