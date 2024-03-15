# Generated by Django 4.2.9 on 2024-03-15 09:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('clinic', '0008_imagingrecord_data_recorder'),
    ]

    operations = [
        migrations.AddField(
            model_name='laboratoryorder',
            name='data_recorder',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='lab_data_recorder', to='clinic.staffs'),
        ),
        migrations.AddField(
            model_name='procedure',
            name='data_recorder',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='procedure_data_recorder', to='clinic.staffs'),
        ),
    ]
