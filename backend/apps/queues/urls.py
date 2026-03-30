from django.urls import path
from .views import QueueViewSet

urlpatterns = [
    path('', QueueViewSet.as_view(), name='queue'),
]