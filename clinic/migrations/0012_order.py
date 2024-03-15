# Generated by Django 4.2.9 on 2024-03-15 15:17

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('clinic', '0011_imagingrecord_result_procedure_result'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_date', models.DateField(blank=True, default=django.utils.timezone.now, null=True)),
                ('order_type', models.CharField(choices=[('Imaging', 'Imaging'), ('Consultation', 'Consultation'), ('Procedure', 'Procedure'), ('Laboratory', 'Laboratory'), ('Ambulance', 'Ambulance')], max_length=100)),
                ('cost', models.DecimalField(decimal_places=2, max_digits=10)),
                ('status', models.CharField(choices=[('Paid', 'Paid'), ('Unpaid', 'Unpaid')], default='Unpaid', max_length=100)),
                ('order_number', models.CharField(max_length=9, unique=True)),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='clinic.patients')),
            ],
        ),
    ]
