# Generated by Django 4.2.9 on 2024-03-06 07:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('clinic', '0015_remove_patients_email_remove_patients_fullname_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patients',
            name='nationality',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='clinic.country'),
        ),
    ]