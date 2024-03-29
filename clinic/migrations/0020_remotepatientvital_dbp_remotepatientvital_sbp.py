# Generated by Django 4.2.9 on 2024-03-16 14:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clinic', '0019_alter_remotepatientvital_temperature'),
    ]

    operations = [
        migrations.AddField(
            model_name='remotepatientvital',
            name='dbp',
            field=models.CharField(blank=True, help_text='Diastolic Blood Pressure (mmHg)', max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='remotepatientvital',
            name='sbp',
            field=models.CharField(blank=True, help_text='Systolic Blood Pressure (mmHg)', max_length=20, null=True),
        ),
    ]
