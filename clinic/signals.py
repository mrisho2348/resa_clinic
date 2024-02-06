# clinic/signals.py

from django.db.models.signals import post_save,pre_save
from django.dispatch import receiver
from .models import InventoryItem, MedicationPayment, MedicineInventory, UsageHistory
from django.db.models import F
from django.db import models

@receiver(post_save, sender=MedicationPayment)
def update_inventory(sender, instance, **kwargs):
    if kwargs.get('created', False) or kwargs.get('update_fields', None):
        # Use F() expression to perform the update in the database
        MedicineInventory.objects.filter(medicine=instance.medicine).update(quantity=F('quantity') - instance.quantity)
        

@receiver(post_save, sender=UsageHistory)
def update_quantity_from_usage_history(sender, instance, **kwargs):
    # Calculate the total quantity used based on associated UsageHistory entries
    total_used = UsageHistory.objects.filter(inventory_item=instance.inventory_item).aggregate(models.Sum('quantity_used'))['quantity_used__sum']
    
    # Update the remaining quantity using an f expression
    InventoryItem.objects.filter(pk=instance.inventory_item.pk).update(remain_quantity=F('quantity') - total_used)