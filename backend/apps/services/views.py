from rest_framework import viewsets
from .serializer import ServiceSerializer
from .models import Service

class ServiceViewSet(viewsets.ModelViewSet):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer