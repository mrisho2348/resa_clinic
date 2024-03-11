# Generated by Django 4.2.9 on 2024-03-10 13:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('clinic', '0025_prescription_entered_by'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='consultation',
            name='pathodology_record',
        ),
        migrations.CreateModel(
            name='ConsultationNotification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_read', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('consultation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='clinic.consultation')),
                ('doctor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='clinic.staffs')),
            ],
            options={
                'verbose_name': 'Consultation Notification',
                'verbose_name_plural': 'Consultation Notifications',
            },
        ),
    ]