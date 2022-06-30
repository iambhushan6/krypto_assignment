
from rest_framework import serializers
from main import models
from django.contrib.auth import get_user_model

class AlertsSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Alert
        fields = [
            "btc_value",
            "direction",
            "status"
            ]