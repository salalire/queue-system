from django.contrib import admin
from . models import QueueEntry

@admin.register(QueueEntry)
class QueueEntryAdmin(admin.ModelAdmin):
    list_display = ('user', 'service', 'position', 'status', 'created_at', 'updated_at', 'snooze_count', 'started_at', 'completed_at')
    list_filter = ('status', 'service')
    search_fields = ('user__username', 'service__name')