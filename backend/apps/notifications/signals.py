from django.db.models.signals import post_save
from django.dispatch import receiver
from apps.queues.models import QueueEntry
from core.utils import send_sms

@receiver(post_save, sender=QueueEntry)
def notify_user_on_queue(sender, instance, created, **kwargs):
    if created:
        message = f"Hello {instance.user.username}, you are at position #{instance.position}."
        send_sms(instance.user.phone, message)

@receiver(post_save, sender=QueueEntry)
def notify_user_when_called(sender, instance, created, **kwargs):
    if not created and instance.status == 'CALLED':
        message = "It is your turn! Please proceed to the counter."
        send_sms(instance.user.phone, message)