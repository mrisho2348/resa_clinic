# Generated by Django 4.2.9 on 2024-04-08 11:09

from django.db import migrations
import django_ckeditor_5.fields


class Migration(migrations.Migration):

    dependencies = [
        ('kahamahmis', '0014_remove_remoteobservationrecord_cost_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='remoteobservationrecord',
            name='description',
        ),
        migrations.AddField(
            model_name='remoteobservationrecord',
            name='observation_notes',
            field=django_ckeditor_5.fields.CKEditor5Field(blank=True, null=True, verbose_name='Text'),
        ),
    ]