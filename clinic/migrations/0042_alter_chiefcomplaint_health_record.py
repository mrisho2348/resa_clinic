# Generated by Django 4.2.9 on 2024-04-01 14:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('clinic', '0041_primaryphysicalexamination_chiefcomplaint'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chiefcomplaint',
            name='health_record',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='clinic.healthrecord'),
        ),
    ]
