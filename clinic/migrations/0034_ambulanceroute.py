# Generated by Django 4.2.9 on 2024-03-27 07:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clinic', '0033_hospitalvehicle'),
    ]

    operations = [
        migrations.CreateModel(
            name='AmbulanceRoute',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('from_location', models.CharField(max_length=100)),
                ('to_location', models.CharField(max_length=100)),
                ('distance', models.FloatField()),
                ('cost', models.DecimalField(decimal_places=2, max_digits=10)),
                ('profit', models.DecimalField(decimal_places=2, max_digits=10)),
                ('advanced_ambulance_cost', models.DecimalField(decimal_places=2, max_digits=10)),
                ('total', models.DecimalField(decimal_places=2, editable=False, max_digits=10)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
