# Generated by Django 4.2.9 on 2024-04-08 12:58

from django.db import migrations, models
import django.db.models.deletion
import django_ckeditor_5.fields


class Migration(migrations.Migration):

    dependencies = [
        ('clinic', '0047_remove_familymedicalhistory_patient_and_more'),
        ('kahamahmis', '0018_rename_doctor_remotereferral_data_recorder_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='RemoteDischargesNotes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('discharge_condition', models.CharField(max_length=255)),
                ('discharge_notes', django_ckeditor_5.fields.CKEditor5Field(blank=True, null=True)),
                ('discharge_date', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('data_recorder', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='clinic.staffs')),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='kahamahmis.remotepatient')),
                ('visit', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='kahamahmis.remotepatientvisits')),
            ],
        ),
    ]
