# Generated by Django 5.1 on 2024-08-20 03:25

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('parking', '0005_alter_parkinghistory_occupancy_rate'),
    ]

    operations = [
        migrations.AddField(
            model_name='hourlyoccupancy',
            name='parking_lot',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='parking.parkinglot'),
            preserve_default=False,
        ),
    ]