# Generated by Django 4.2.9 on 2024-01-26 00:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('clinic', '0015_referral'),
    ]

    operations = [
        migrations.RenameField(
            model_name='payment',
            old_name='insurance_id',
            new_name='insurance',
        ),
        migrations.RenameField(
            model_name='payment',
            old_name='patient_id',
            new_name='patient',
        ),
        migrations.AddField(
            model_name='consultation',
            name='pathodology_record',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='clinic.pathodologyrecord'),
        ),
        migrations.AddField(
            model_name='diseaserecode',
            name='related_pathology_records',
            field=models.ManyToManyField(blank=True, to='clinic.pathodologyrecord'),
        ),
        migrations.AddField(
            model_name='pathodologyrecord',
            name='related_diseases',
            field=models.ManyToManyField(blank=True, to='clinic.diseaserecode'),
        ),
        migrations.CreateModel(
            name='PatientDisease',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('diagnosis_date', models.DateField()),
                ('severity', models.CharField(max_length=50)),
                ('treatment_plan', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('disease_record', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='clinic.diseaserecode')),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='diseases', to='clinic.patients')),
            ],
        ),
        migrations.CreateModel(
            name='MedicationPayment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('non_registered_patient_name', models.CharField(blank=True, max_length=255, null=True)),
                ('non_registered_patient_email', models.EmailField(blank=True, max_length=254, null=True)),
                ('non_registered_patient_phone', models.CharField(blank=True, max_length=15, null=True)),
                ('quantity', models.PositiveIntegerField()),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('payment_date', models.DateField()),
                ('medicine', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='clinic.medicine')),
                ('patient', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='clinic.patients')),
            ],
        ),
        migrations.CreateModel(
            name='DiagnosticTest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('test_id', models.CharField(editable=False, max_length=12, unique=True)),
                ('test_type', models.CharField(max_length=255)),
                ('test_date', models.DateField()),
                ('result', models.TextField(blank=True, null=True)),
                ('diseases', models.ManyToManyField(to='clinic.diseaserecode')),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='diagnostic_tests', to='clinic.patients')),
            ],
        ),
        migrations.CreateModel(
            name='ConsultationFee',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fee_amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('consultation_date', models.DateField()),
                ('doctor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='clinic.staffs')),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='clinic.patients')),
            ],
        ),
        migrations.AddField(
            model_name='consultation',
            name='cost',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='clinic.consultationfee'),
        ),
    ]
