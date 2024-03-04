# Generated by Django 4.2.9 on 2024-03-03 11:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clinic', '0012_remove_patientsurgery_hospital_name_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='remotepatient',
            name='emergency_contact_relation',
        ),
        migrations.AddField(
            model_name='remotepatient',
            name='other_emergency_contact_relation',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='remotepatient',
            name='other_insurance_company',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='remotepatient',
            name='other_occupation',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='remotepatient',
            name='other_patient_type',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]