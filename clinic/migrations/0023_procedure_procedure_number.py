# Generated by Django 4.2.9 on 2024-03-08 10:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clinic', '0022_alter_consultation_appointment_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='procedure',
            name='procedure_number',
            field=models.CharField(default='PR-0000000', max_length=20, unique=True),
        ),
    ]