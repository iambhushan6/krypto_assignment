# Generated by Django 4.0.5 on 2022-06-30 19:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='alert',
            name='direction',
            field=models.CharField(choices=[('above', 'Above'), ('below', 'Below')], default='above', max_length=20),
        ),
    ]
