# Generated by Django 4.2.9 on 2024-03-27 07:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clinic', '0034_ambulanceroute'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ambulanceroute',
            name='total',
            field=models.FloatField(editable=False),
        ),
    ]
