# Generated by Django 4.2.9 on 2024-03-29 15:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clinic', '0038_rename_cost_service_cash_cost_service_insurance_cost_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='MedicineRoute',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('explanation', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='MedicineUnitMeasure',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('short_name', models.CharField(max_length=20)),
                ('application_user', models.CharField(max_length=100)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]