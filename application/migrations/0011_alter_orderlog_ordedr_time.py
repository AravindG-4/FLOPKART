# Generated by Django 5.0.4 on 2024-05-20 16:32

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0010_remove_product_size_productimage_is_main_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderlog',
            name='ordedr_time',
            field=models.DateTimeField(default=datetime.datetime(2024, 5, 20, 22, 2, 0, 92587)),
        ),
    ]
