# Generated by Django 4.2.9 on 2024-02-26 14:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clinic', '0003_alter_labtest_diagnosis'),
    ]

    operations = [
        migrations.AlterField(
            model_name='labtest',
            name='lab_number',
            field=models.CharField(max_length=20, unique=True, verbose_name='Lab Number'),
        ),
    ]
