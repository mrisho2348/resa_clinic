# Generated by Django 4.2.9 on 2024-03-16 10:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clinic', '0017_order_doctor_order_is_read'),
    ]

    operations = [
        migrations.AddField(
            model_name='ambulanceorder',
            name='order_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]
