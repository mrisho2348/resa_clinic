# Generated by Django 4.2.9 on 2024-01-21 23:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clinic', '0009_notification_is_read_notification_updated_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='consultation',
            name='status',
            field=models.IntegerField(choices=[(0, 'Pending'), (1, 'Completed'), (2, 'Canceled'), (3, 'Rescheduled'), (4, 'No-show'), (5, 'In Progress'), (6, 'Confirmed'), (7, 'Arrived')], default=0),
        ),
    ]
