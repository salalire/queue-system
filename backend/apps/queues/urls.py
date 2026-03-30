from django.urls import path
from .views import JoinQueueView, LeaveQueueView, MyQueueStatusView, ServeNextView

urlpatterns = [
    path('join/', JoinQueueView.as_view(), name='join-queue'),
    path('status/', MyQueueStatusView.as_view()),
     path('leave/', LeaveQueueView.as_view()),
     path('serve-next/', ServeNextView.as_view()),
]