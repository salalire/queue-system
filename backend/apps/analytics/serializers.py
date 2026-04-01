from rest_framework import serializers
from .models import ServiceAnalytics
from apps.services.models import Service

class AnalyticsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceAnalytics
        fields = '__all__'