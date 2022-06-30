from statistics import mode
from django.db import models
from authentication.models import User

# Create your models here.


class Alert(models.Model):

    class AlertDirection(models.TextChoices):
        ABOVE = "above"
        BELOW = "below"
    
    class AlertStatus(models.TextChoices):
        CREATED = "created"
        DELETED = "deleted"
        TRIGGERED = "triggered"

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    btc_value = models.PositiveBigIntegerField(unique=True)
    direction = models.CharField(choices=AlertDirection.choices, max_length=20, default=AlertDirection.ABOVE)
    status = models.CharField(max_length=20,choices=AlertStatus.choices, null=True,blank=True)


class AlertTracking(models.Model):
    alert = models.ForeignKey(Alert, on_delete=models.CASCADE)
    mail_sent = models.BooleanField()
