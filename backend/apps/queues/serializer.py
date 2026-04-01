from rest_framework import serializers
from .models import QueueEntry
from apps.services.models import Service
from core.utils import calculate_wait_time


class JoinQueueSerializer(serializers.ModelSerializer):
    service_name = serializers.CharField(write_only=True)

    class Meta:
        model = QueueEntry
        fields = ['id', 'service_name', 'position', 'user', 'status', 'snooze_count', 'started_at', 'completed_at']
        read_only_fields = ['id', 'position']

    def validate_service_name(self, value):
        if not Service.objects.filter(name__iexact=value, is_active=True).exists():
            raise serializers.ValidationError(f"Service '{value}' is not available.")
        return value

    def create(self, validated_data):
        request = self.context['request']
        user = request.user

        service_name = validated_data.pop('service_name')
        service = Service.objects.get(name__iexact=service_name)

        current_queue = QueueEntry.objects.filter(
            service=service,
            status='waiting'
        ).count()

        position = current_queue + 1
        wait_time = calculate_wait_time(service, position)
        queue_entry = QueueEntry.objects.create(
            user=user,
            service=service,
            position=position,
            wait_time=wait_time
        )

        return queue_entry