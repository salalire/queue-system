from rest_framework import serializers
from .models import QueueEntry
from apps.services.models import Service


class JoinQueueSerializer(serializers.ModelSerializer):
    service_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = QueueEntry
        fields = ['id', 'service_id']

    def validate_service_id(self, value):
        if not Service.objects.filter(id=value, is_active=True).exists():
            raise serializers.ValidationError("Service not available")
        return value

    def create(self, validated_data):
        request = self.context['request']
        user = request.user

        service = Service.objects.get(id=validated_data['service_id'])

        # Get current queue length for that service
        current_queue = QueueEntry.objects.filter(
            service=service,
            status='waiting'
        ).count()

        position = current_queue + 1

        queue_entry = QueueEntry.objects.create(
            user=user,
            service=service,
            position=position
        )

        return queue_entry