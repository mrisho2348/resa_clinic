# Generated by Django 4.2.9 on 2024-02-18 09:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('clinic', '0003_alter_prescription_total_price'),
    ]

    operations = [
        migrations.CreateModel(
            name='PatientVital',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('recorded_at', models.DateTimeField(auto_now_add=True)),
                ('respiratory_rate', models.DecimalField(blank=True, decimal_places=2, help_text='Respiratory rate in breaths per minute', max_digits=5, null=True)),
                ('pulse_rate', models.PositiveIntegerField(blank=True, help_text='Pulse rate in beats per minute', null=True)),
                ('blood_pressure', models.CharField(blank=True, help_text='Blood pressure measurement', max_length=20, null=True)),
                ('spo2', models.DecimalField(blank=True, decimal_places=2, help_text='SPO2 measurement in percentage', max_digits=5, null=True)),
                ('temperature', models.DecimalField(blank=True, decimal_places=2, help_text='Temperature measurement in Celsius', max_digits=5, null=True)),
                ('gcs', models.PositiveIntegerField(blank=True, help_text='Glasgow Coma Scale measurement', null=True)),
                ('avpu', models.CharField(blank=True, help_text='AVPU scale measurement', max_length=10, null=True)),
                ('unique_identifier', models.CharField(editable=False, max_length=10, unique=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='clinic.patients')),
            ],
        ),
    ]
