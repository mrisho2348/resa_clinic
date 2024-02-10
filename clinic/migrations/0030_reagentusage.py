# Generated by Django 4.2.9 on 2024-02-10 10:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('clinic', '0029_reagent'),
    ]

    operations = [
        migrations.CreateModel(
            name='ReagentUsage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('usage_date', models.DateField()),
                ('quantity_used', models.PositiveIntegerField()),
                ('observation', models.TextField()),
                ('technician_notes', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('lab_technician', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='clinic.staffs')),
                ('reagent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='clinic.reagent')),
            ],
        ),
    ]
