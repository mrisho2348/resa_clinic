# Generated by Django 4.2.9 on 2024-01-19 00:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('clinic', '0002_remove_staffs_address'),
    ]

    operations = [
        migrations.CreateModel(
            name='Patient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mrn_format', models.CharField(max_length=20)),
                ('first_name', models.CharField(max_length=50)),
                ('middle_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('gender', models.CharField(max_length=10)),
                ('age', models.PositiveIntegerField()),
                ('nationality', models.CharField(max_length=50)),
                ('patient_type', models.CharField(max_length=20)),
                ('company', models.CharField(max_length=50)),
                ('occupation', models.CharField(max_length=50)),
                ('phone', models.CharField(max_length=15)),
                ('employee_number', models.CharField(max_length=20)),
                ('date_of_first_employment', models.DateField()),
                ('long_time_illness', models.TextField()),
                ('long_time_medication', models.TextField()),
                ('osha_certificate', models.BooleanField(default=False)),
                ('osha_date', models.DateField(blank=True, null=True)),
                ('insurance', models.CharField(choices=[('Uninsured', 'Uninsured'), ('Insured', 'Insured')], max_length=20)),
                ('insurance_name', models.CharField(blank=True, max_length=50, null=True)),
                ('insurance_number', models.IntegerField(blank=True, null=True)),
                ('emergency_contact_name', models.CharField(max_length=50)),
                ('emergency_contact_relation', models.CharField(max_length=50)),
                ('emergency_contact_phone', models.CharField(max_length=15)),
                ('emergency_contact_mobile', models.CharField(max_length=15)),
                ('allergies', models.BooleanField(default=False)),
                ('allergies_notes', models.TextField()),
                ('eye_condition', models.BooleanField(default=False)),
                ('eye_condition_notes', models.TextField()),
                ('ent_conditions', models.BooleanField(default=False)),
                ('ent_conditions_notes', models.TextField()),
                ('respiratory_conditions', models.BooleanField(default=False)),
                ('respiratory_conditions_notes', models.TextField()),
                ('cardiovascular_conditions', models.BooleanField(default=False)),
                ('cardiovascular_conditions_notes', models.TextField()),
                ('urinary_conditions', models.BooleanField(default=False)),
                ('urinary_conditions_notes', models.TextField()),
                ('stomach_bowel_conditions', models.BooleanField(default=False)),
                ('stomach_bowel_conditions_notes', models.TextField()),
                ('musculoskeletal_conditions', models.BooleanField(default=False)),
                ('musculoskeletal_conditions_notes', models.TextField()),
                ('neuro_psychiatric_conditions', models.BooleanField(default=False)),
                ('neuro_psychiatric_conditions_notes', models.TextField()),
                ('family_allergies', models.BooleanField(default=False)),
                ('family_allergies_relationship', models.CharField(blank=True, max_length=50)),
                ('family_allergies_comments', models.TextField(blank=True)),
                ('family_asthma_condition', models.BooleanField(default=False)),
                ('family_asthma_condition_relationship', models.CharField(blank=True, max_length=50)),
                ('family_asthma_condition_comments', models.TextField(blank=True)),
                ('family_lungdisease_conditions', models.BooleanField(default=False)),
                ('family_lungdisease_conditions_relationship', models.CharField(blank=True, max_length=50)),
                ('family_lungdisease_conditions_comments', models.TextField(blank=True)),
                ('family_diabetes_conditions', models.BooleanField(default=False)),
                ('family_diabetes_conditions_relationship', models.CharField(blank=True, max_length=50)),
                ('family_diabetes_conditions_comments', models.TextField(blank=True)),
                ('family_cancer_conditions', models.BooleanField(default=False)),
                ('family_cancer_conditions_relationship', models.CharField(blank=True, max_length=50)),
                ('family_cancer_conditions_comments', models.TextField(blank=True)),
                ('family_hypertension_conditions', models.BooleanField(default=False)),
                ('family_hypertension_conditions_relationship', models.CharField(blank=True, max_length=50)),
                ('family_hypertension_conditions_comments', models.TextField(blank=True)),
                ('family_heart_disease_conditions', models.BooleanField(default=False)),
                ('family_heart_disease_conditions_relationship', models.CharField(blank=True, max_length=50)),
                ('family_heart_disease_conditions_comments', models.TextField(blank=True)),
                ('smoking', models.BooleanField(default=False)),
                ('alcohol_consumption', models.BooleanField(default=False)),
                ('weekly_exercise_frequency', models.CharField(max_length=50)),
                ('healthy_diet', models.BooleanField(default=False)),
                ('stress_management', models.BooleanField(default=False)),
                ('sufficient_sleep', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='MedicalRecordConsultation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('chief_complaint', models.CharField(max_length=255)),
                ('history_illness', models.TextField()),
                ('physical_examination', models.TextField()),
                ('allergy_medications', models.TextField()),
                ('provisional_diagnosis', models.TextField()),
                ('final_diagnosis', models.TextField()),
                ('plan', models.TextField()),
                ('injury', models.CharField(max_length=200)),
                ('fatality', models.CharField(max_length=200)),
                ('injury_description', models.TextField()),
                ('disposition', models.CharField(max_length=200)),
                ('destination', models.CharField(max_length=255)),
                ('disposition_description', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('pathology', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='clinic.pathodologyrecord')),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='clinic.patient')),
            ],
        ),
        migrations.CreateModel(
            name='Appointment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('appointment_date', models.DateField()),
                ('start_time', models.TimeField()),
                ('end_time', models.TimeField()),
                ('description', models.TextField()),
                ('doctor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='clinic.staffs')),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='clinic.patient')),
            ],
        ),
    ]