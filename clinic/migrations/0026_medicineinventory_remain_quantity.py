# Generated by Django 4.2.9 on 2024-02-09 01:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clinic', '0025_category_inventoryitem_supplier_usagehistory_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='medicineinventory',
            name='remain_quantity',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
