# Generated by Django 4.2.9 on 2024-01-26 00:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('clinic', '0016_rename_insurance_id_payment_insurance_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='HealthIssue',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('is_disease', models.BooleanField(default=True)),
                ('severity', models.CharField(blank=True, max_length=50, null=True)),
                ('treatment_plan', models.TextField(blank=True, null=True)),
                ('onset_date', models.DateField(blank=True, null=True)),
                ('resolution_date', models.DateField(blank=True, null=True)),
            ],
        ),
        migrations.AddField(
            model_name='diagnostictest',
            name='pathology_record',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='clinic.pathodologyrecord'),
        ),
        migrations.AddField(
            model_name='diagnostictest',
            name='health_issues',
            field=models.ManyToManyField(to='clinic.healthissue'),
        ),
    ]
