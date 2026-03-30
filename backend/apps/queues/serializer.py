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

    def validate(self, attrs):
        user = self.context['request'].user
        service_id = attrs['service_id']
        # Prevent duplicate active queue entry for same service
        already_in_queue = QueueEntry.objects.filter(
            user=user,
            service_id=service_id,
            status__in=['waiting', 'serving']
        ).exists()
        if already_in_queue:
            raise serializers.ValidationError("You are already in the queue for this service")
        return attrs

    def create(self, validated_data):
        request = self.context['request']
        user = request.user
        service = Service.objects.get(id=validated_data['service_id'])

        position = QueueEntry.objects.filter(
            service=service,
            status='waiting'
        ).count() + 1

        return QueueEntry.objects.create(
            user=user,
            service=service,
            position=position
        )


class QueueStatusSerializer(serializers.ModelSerializer):
    service_name = serializers.CharField(source='service.name')

    class Meta:
        model = QueueEntry
        fields = ['id', 'service_name', 'position', 'status', 'joined_at']
