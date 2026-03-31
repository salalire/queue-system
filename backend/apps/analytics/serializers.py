from rest_framework import serializers
from .models import ServiceAnalytics

class AnalyticsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceAnalytics
        fields = ['id', 'service', 'date', 'total_joined', 'total_served', 'total_cancelled', 'avg_wait_time']
        read_only_fields = ['id']