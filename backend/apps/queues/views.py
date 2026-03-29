from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated

from .serializer import JoinQueueSerializer
from core.utils import calculate_wait_time


class JoinQueueView(APIView):

    permission_classes = [AllowAny]

    def post(self, request):
        serializer = JoinQueueSerializer(
            data=request.data,
            context={'request': request}
        )

        if serializer.is_valid():
            queue_entry = serializer.save()

            wait_time = calculate_wait_time(
                queue_entry.service,
                queue_entry.position
            )

            return Response({
                "message": "Joined queue successfully",
                "queue_id": queue_entry.id,
                "position": queue_entry.position,
                "estimated_wait_time": wait_time,
                "status": queue_entry.status
            }, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Create your views here.
