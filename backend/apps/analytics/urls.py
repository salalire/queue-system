from django.urls import path
from .views import ServiceAnalyticsView, AllServicesAnalyticsView

urlpatterns = [
    path('', AllServicesAnalyticsView.as_view(), name='all-analytics'),
    path('<int:service_id>/', ServiceAnalyticsView.as_view(), name='service-analytics'),
]
