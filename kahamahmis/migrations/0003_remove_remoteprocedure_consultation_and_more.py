# Generated by Django 4.2.9 on 2024-04-03 13:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('clinic', '0047_remove_familymedicalhistory_patient_and_more'),
        ('kahamahmis', '0002_remove_remotereferral_consultation_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='remoteprocedure',
            name='consultation',
        ),
        migrations.RemoveField(
            model_name='remoteprocedure',
            name='duration_time',
        ),
        migrations.RemoveField(
            model_name='remoteprocedure',
            name='equipments_used',
        ),
        migrations.AlterField(
            model_name='remoteprocedure',
            name='name',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='clinic.service'),
        ),
    ]
