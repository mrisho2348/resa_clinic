# clinic/signals.py

from django.db.models.signals import post_save,pre_save
from django.dispatch import receiver
from .models import MedicationPayment, MedicineInventory
from django.db.models import F
from django.db import models

@receiver(post_save, sender=MedicationPayment)
def update_inventory(sender, instance, **kwargs):
    if kwargs.get('created', False) or kwargs.get('update_fields', None):
        # Use F() expression to perform the update in the database
        MedicineInventory.objects.filter(medicine=instance.medicine).update(quantity=F('quantity') - instance.quantity)
        

