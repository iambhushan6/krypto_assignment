
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import ListCreateAPIView
from main.models import Alert
from main.serializers import AlertsSerializer
from main.permissions import IsOwner
from rest_framework.permissions import IsAuthenticated
from django.core.cache import cache
# Create your views here.


class AlertsAPIView(ListCreateAPIView):

    permission_classes = [IsAuthenticated, IsOwner]
    serializer_class = AlertsSerializer

    def get(self, request, format=None):

        if cache.get('alert'):
            serialized_data = cache.get('alert')
        else:
            data = Alert.objects.filter(user=self.request.user)
            serializer = AlertsSerializer(data, many=True)
            serialized_data = serializer.data
            cache.set('alert', serialized_data, timeout=10)

        return Response(serialized_data)

    def post(self, request, format=None):

        serializer = AlertsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=self.request.user,
                            status=Alert.AlertStatus.CREATED)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
