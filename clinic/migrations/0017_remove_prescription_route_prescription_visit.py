# Generated by Django 4.2.9 on 2024-03-07 12:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('clinic', '0016_alter_patients_nationality'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='prescription',
            name='route',
        ),
        migrations.AddField(
            model_name='prescription',
            name='visit',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='clinic.patientvisits'),
        ),
    ]
