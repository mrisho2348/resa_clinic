# Generated by Django 4.2.9 on 2024-03-13 16:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clinic', '0003_imagingrecord_order_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='procedure',
            name='order_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]
