# Generated by Django 5.0.4 on 2024-05-20 13:23

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0006_alter_orderlog_ordedr_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='brand',
            name='email',
            field=models.EmailField(default=None, max_length=254),
        ),
        migrations.AlterField(
            model_name='orderlog',
            name='ordedr_time',
            field=models.DateTimeField(default=datetime.datetime(2024, 5, 20, 18, 53, 24, 779044)),
        ),
    ]
