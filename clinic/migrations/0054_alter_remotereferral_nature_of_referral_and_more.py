# Generated by Django 4.2.9 on 2024-04-13 16:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clinic', '0053_remoteconsultationnotes_nature_of_current_illness_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='remotereferral',
            name='nature_of_referral',
            field=models.CharField(choices=[('Med Evac', 'Med Evac'), ('Referral', 'Referral')], default='referral', max_length=20),
        ),
        migrations.AlterField(
            model_name='remotereferral',
            name='transport_model',
            field=models.CharField(choices=[('Ground Ambulance', 'Ground Ambulance'), ('Air Ambulance', 'Air Ambulance'), ('Private Vehicle', 'Private Vehicle'), ('Self Transport', 'Self Transport'), ('Company Walking', 'Company Walking'), ('Walking', 'Walking'), ('Motorcycle', 'Motorcycle'), ('Others', 'Others'), ('Unknown', 'Unknown')], default='ground_ambulance', max_length=50),
        ),
    ]
