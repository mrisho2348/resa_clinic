# Generated by Django 4.2.9 on 2024-02-28 15:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('clinic', '0007_alter_remotepatientvital_visit'),
    ]

    operations = [
        migrations.AlterField(
            model_name='remoteconsultationnotes',
            name='visit',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='clinic.remotepatientvisits'),
        ),
    ]
