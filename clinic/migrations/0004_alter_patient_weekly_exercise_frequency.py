# Generated by Django 4.2.9 on 2024-01-19 00:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clinic', '0003_patient_medicalrecordconsultation_appointment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patient',
            name='weekly_exercise_frequency',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
