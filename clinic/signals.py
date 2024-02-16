# clinic/signals.py

from django.db.models.signals import post_save,pre_save
from django.dispatch import receiver
from .models import InventoryItem, MedicationPayment, MedicineInventory, Prescription, Reagent, ReagentUsage, UsageHistory
from django.db.models import F
from django.db import models

@receiver(post_save, sender=MedicationPayment)
def update_inventory(sender, instance, **kwargs):
    if kwargs.get('created', False) or kwargs.get('update_fields', None):
        # Use F() expression to perform the update in the database
        MedicineInventory.objects.filter(medicine=instance.medicine).update(remain_quantity=F('remain_quantity') - instance.quantity)
        

@receiver(post_save, sender=MedicineInventory)
def update_total_payment(sender, instance, created, **kwargs):
    if created:
        # Calculate total payment for the inventory
        total_payment = instance.quantity * instance.medicine.unit_price
        
        # Update the total_payment field of the MedicineInventory instance
        instance.total_payment = total_payment
        instance.save(update_fields=['total_payment'])  
              
@receiver(post_save, sender=Prescription)
def update_total_payment_per_prescription(sender, instance, created, **kwargs):
    if created:
        # Calculate total payment for the inventory
        total_price = instance.quantity * instance.medicine.unit_price
        
        # Update the total_payment field of the MedicineInventory instance
        instance.total_price = total_price
        instance.save(update_fields=['total_price'])        
        
@receiver(post_save, sender=ReagentUsage)
def update_reagent_usage(sender, instance, **kwargs):
    if kwargs.get('created', False) or kwargs.get('update_fields', None):
        # Use F() expression to perform the update in the database
        Reagent.objects.filter(id=instance.reagent_id).update(remaining_quantity=F('remaining_quantity') - instance.quantity_used)
        

@receiver(post_save, sender=UsageHistory)
def update_quantity_from_usage_history(sender, instance, **kwargs):
    # Calculate the total quantity used based on associated UsageHistory entries
    total_used = UsageHistory.objects.filter(inventory_item=instance.inventory_item).aggregate(models.Sum('quantity_used'))['quantity_used__sum']
    
    # Update the remaining quantity using an f expression
    InventoryItem.objects.filter(pk=instance.inventory_item.pk).update(remain_quantity=F('quantity') - total_used)
    
@receiver(post_save, sender=Prescription)
def update_medicine_inventory_per_prescription(sender, instance, created, **kwargs):
    if created:
        # Deduct quantity from MedicineInventory when a new Prescription is created
        try:
            medicine_inventory = MedicineInventory.objects.get(medicine=instance.drug)
            medicine_inventory.remain_quantity -= instance.quantity
            medicine_inventory.save()
        except MedicineInventory.DoesNotExist:
            # Handle if medicine inventory does not exist
            pass    
    