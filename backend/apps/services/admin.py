from django.contrib import admin

from .models import Service
@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'priority_level', 'avg_service_time', 'is_active', 'created_at')
    list_filter = ('is_active', 'priority_level')
    search_fields = ('name', 'description')
