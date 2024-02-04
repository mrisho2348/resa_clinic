# Generated by Django 4.2.9 on 2024-02-01 00:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clinic', '0019_alter_sample_collection_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sample',
            name='status',
            field=models.CharField(choices=[('collected', 'Collected'), ('processing', 'Processing'), ('analyzed', 'Analyzed')], default='collected', max_length=20),
        ),
    ]