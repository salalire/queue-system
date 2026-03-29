from django.urls import path
from .views import JoinQueueView

urlpatterns = [
    path('join/', JoinQueueView.as_view(), name='join-queue'),
]