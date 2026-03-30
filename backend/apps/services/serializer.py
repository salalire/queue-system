from rest_framework import serializers
from .models import Service

class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = ['name', 'description', 'priority_level', 'avg_service_time', 'is_active']
        read_only_fields = ['id']