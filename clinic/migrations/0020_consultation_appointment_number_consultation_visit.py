# Generated by Django 4.2.9 on 2024-03-08 07:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('clinic', '0019_patientvital_weight'),
    ]

    operations = [
        migrations.AddField(
            model_name='consultation',
            name='appointment_number',
            field=models.CharField(default='APT-0000000', max_length=20, unique=True),
        ),
        migrations.AddField(
            model_name='consultation',
            name='visit',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='clinic.patientvisits'),
        ),
    ]