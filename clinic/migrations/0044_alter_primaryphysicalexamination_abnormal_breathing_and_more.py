# Generated by Django 4.2.9 on 2024-04-02 11:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clinic', '0043_primaryphysicalexamination_created_at_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='primaryphysicalexamination',
            name='abnormal_breathing',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='primaryphysicalexamination',
            name='abnormal_circulating',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='primaryphysicalexamination',
            name='abnormal_exposure',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='primaryphysicalexamination',
            name='avpu',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='primaryphysicalexamination',
            name='breathing',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='primaryphysicalexamination',
            name='circulating',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='primaryphysicalexamination',
            name='exposure',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='primaryphysicalexamination',
            name='gcs',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='primaryphysicalexamination',
            name='normal_breathing',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='primaryphysicalexamination',
            name='normal_circulating',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='primaryphysicalexamination',
            name='normal_exposure',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='primaryphysicalexamination',
            name='notpatient_explanation',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='primaryphysicalexamination',
            name='pain_score',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='primaryphysicalexamination',
            name='patent_airway',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='primaryphysicalexamination',
            name='pupil',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='primaryphysicalexamination',
            name='rbg',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
