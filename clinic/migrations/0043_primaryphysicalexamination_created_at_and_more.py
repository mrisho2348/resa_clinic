# Generated by Django 4.2.9 on 2024-04-02 11:29

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('clinic', '0042_alter_chiefcomplaint_health_record'),
    ]

    operations = [
        migrations.AddField(
            model_name='primaryphysicalexamination',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='primaryphysicalexamination',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.CreateModel(
            name='SecondaryPhysicalExamination',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('heent', models.CharField(blank=True, max_length=50, null=True)),
                ('cns', models.CharField(blank=True, max_length=50, null=True)),
                ('normal_cns', models.CharField(blank=True, max_length=50, null=True)),
                ('abnormal_cns', models.CharField(blank=True, max_length=50, null=True)),
                ('cvs', models.CharField(blank=True, max_length=50, null=True)),
                ('normal_cvs', models.CharField(blank=True, max_length=50, null=True)),
                ('abnormal_cvs', models.CharField(blank=True, max_length=50, null=True)),
                ('rs', models.CharField(blank=True, max_length=50, null=True)),
                ('normal_rs', models.CharField(blank=True, max_length=50, null=True)),
                ('abnormal_rs', models.CharField(blank=True, max_length=50, null=True)),
                ('pa', models.CharField(blank=True, max_length=50, null=True)),
                ('normal_pa', models.CharField(blank=True, max_length=50, null=True)),
                ('abnormal_pa', models.CharField(blank=True, max_length=50, null=True)),
                ('gu', models.CharField(blank=True, max_length=100, null=True)),
                ('normal_gu', models.CharField(blank=True, max_length=100, null=True)),
                ('abnormal_gu', models.CharField(blank=True, max_length=100, null=True)),
                ('mss', models.CharField(blank=True, max_length=100, null=True)),
                ('normal_mss', models.CharField(blank=True, max_length=100, null=True)),
                ('abnormal_mss', models.CharField(blank=True, max_length=100, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='clinic.remotepatient')),
                ('visit', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='clinic.remotepatientvisits')),
            ],
        ),
    ]
