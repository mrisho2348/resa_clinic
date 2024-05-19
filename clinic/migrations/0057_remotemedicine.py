# Generated by Django 4.2.9 on 2024-04-15 09:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clinic', '0056_diagnosis_diagnosis_code'),
    ]

    operations = [
        migrations.CreateModel(
            name='RemoteMedicine',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('drug_name', models.CharField(max_length=100)),
                ('drug_type', models.CharField(choices=[('Tablet', 'Tablet'), ('Capsule', 'Capsule'), ('Syrup', 'Syrup'), ('Injection', 'Injection'), ('Ointment', 'Ointment'), ('Drops', 'Drops'), ('Inhaler', 'Inhaler'), ('Patch', 'Patch'), ('Liquid', 'Liquid'), ('Cream', 'Cream'), ('Gel', 'Gel'), ('Suppository', 'Suppository'), ('Powder', 'Powder'), ('Lotion', 'Lotion'), ('Suspension', 'Suspension'), ('Lozenge', 'Lozenge')], max_length=20)),
                ('formulation_unit', models.CharField(max_length=50)),
                ('manufacturer', models.CharField(max_length=100)),
                ('remain_quantity', models.PositiveIntegerField(blank=True, null=True)),
                ('quantity', models.PositiveIntegerField(blank=True, null=True)),
                ('dividable', models.CharField(blank=True, max_length=20, null=True)),
                ('batch_number', models.CharField(blank=True, max_length=20, null=True)),
                ('expiration_date', models.DateField()),
                ('unit_cost', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('buying_price', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]