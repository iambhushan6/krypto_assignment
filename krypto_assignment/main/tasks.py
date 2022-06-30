import requests
from main.models import Alert
from django.core.mail import send_mail
from krypto_assignment import settings
from krypto_assignment.celery import app
from celery.schedules import crontab

@app.task()
def scheduled_send_mail_for_alerts(self):

    data = requests.get(settings.BTC_URL)       # Fetch bitcoin data for url

    if data:
        current_bitcoin_value = data[0].get("current_price")

        alerts = Alert.objects.filter(btc_value__lte=current_bitcoin_value,direction=Alert.AlertDirection.BELOW)

        user_mail_list = [ alert.user.email for alert in alerts ]

        for user_mail in user_mail_list:
            mail_subject = "BTC Value drop alert from KRYPTO"
            message = f"Your alert from Krypto: BTC value has dropped below {current_bitcoin_value}"
            to_email = user_mail
            send_mail(
                subject = mail_subject,
                message=message,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[to_email],
                fail_silently=True,
            )

        alerts.update(status=Alert.AlertStatus.TRIGGERED)

        alerts = Alert.objects.filter(btc_value__gte=current_bitcoin_value,direction=Alert.AlertDirection.ABOVE)
        user_mail_list = [ alert.user.email for alert in alerts ]

        for user_mail in user_mail_list:
            mail_subject = "BTC Value surge alert from KRYPTO"
            message = f"Your alert from Krypto: BTC value has surged above {current_bitcoin_value}"
            to_email = user_mail
            send_mail(
                subject = mail_subject,
                message=message,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[to_email],
                fail_silently=True,
            )
        alerts.update(status=Alert.AlertStatus.TRIGGERED)
        

# I have made this task as for now scheduled we can make without scheduling as well

app.conf.beat_schedule = {
    "send_mail_for_alerts_every_minute": {
        "task": "krypto_assignment.main.tasks.scheduled_send_mail_for_alerts",
        "schedule": crontab(minute='*/1'),
        "args": (),
    }
}