# clinic/signals.py

from django.db.models.signals import post_save,pre_save
from django.dispatch import receiver


from .models import AmbulanceOrder, Consultation, ConsultationNotification, ConsultationOrder, ImagingRecord, InventoryItem, LaboratoryOrder, MedicationPayment, MedicineInventory, Order, Prescription, Procedure, Reagent, ReagentUsage, RemotePrescription, UsageHistory
from django.db.models import F
from django.db import models

@receiver(post_save, sender=MedicationPayment)
def update_inventory(sender, instance, **kwargs):
    if kwargs.get('created', False) or kwargs.get('update_fields', None):
        # Use F() expression to perform the update in the database
        MedicineInventory.objects.filter(medicine=instance.medicine).update(remain_quantity=F('remain_quantity') - instance.quantity)
        


@receiver(post_save, sender=Consultation)
def create_consultation_notification(sender, instance, created, **kwargs):
    if created:
        # Create a ConsultationNotification object for the newly created Consultation
        ConsultationNotification.objects.create(
            consultation=instance,
            doctor=instance.doctor,
            is_read=False  # Default to unread
        )
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
        total_price = instance.quantity_used * instance.medicine.unit_price        
        # Update the total_payment field of the MedicineInventory instance
        instance.total_price = total_price
        instance.save(update_fields=['total_price']) 
               
@receiver(post_save, sender=RemotePrescription)
def update_total_payment_prescription(sender, instance, created, **kwargs):
    if created:
        # Calculate total payment for the inventory
        total_price = instance.quantity_used * instance.medicine.cash_cost
        
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
            medicine_inventory = MedicineInventory.objects.get(medicine=instance.medicine)
            medicine_inventory.remain_quantity -= instance.quantity_used
            medicine_inventory.save()
        except MedicineInventory.DoesNotExist:
            # Handle if medicine inventory does not exist
            pass    
@receiver(post_save, sender=RemotePrescription)
def update_medicine_inventory_prescription(sender, instance, created, **kwargs):
    if created:
        # Deduct quantity from MedicineInventory when a new Prescription is created
        try:
            medicine_inventory = MedicineInventory.objects.get(medicine=instance.medicine)
            medicine_inventory.remain_quantity -= instance.quantity_used
            medicine_inventory.save()
        except MedicineInventory.DoesNotExist:
            # Handle if medicine inventory does not exist
            pass    
    
    
@receiver(post_save, sender=ImagingRecord)
def create_imaging_order(sender, instance, created, **kwargs):
    if created:
        Order.objects.create(
            order_date=instance.order_date,
            order_type=instance.imaging.name,
            patient=instance.patient,
            doctor=instance.doctor,
            visit=instance.visit,
            added_by=instance.data_recorder,
            cost=instance.cost,
        )

@receiver(post_save, sender=ConsultationOrder)
def create_consultation_order(sender, instance, created, **kwargs):
    if created:
        Order.objects.create(
            order_date=instance.order_date,
            order_type=instance.consultation.name,
            patient=instance.patient,
            doctor=instance.doctor,
            visit=instance.visit,
            added_by=instance.data_recorder,
            cost=instance.cost,
        )

@receiver(post_save, sender=Procedure)
def create_procedure_order(sender, instance, created, **kwargs):
    if created:
        Order.objects.create(
            order_date=instance.order_date,
            order_type=instance.name.name,
            patient=instance.patient,
            doctor=instance.doctor,
            visit=instance.visit,
            added_by=instance.data_recorder,
            cost=instance.cost,
        )

@receiver(post_save, sender=LaboratoryOrder)
def create_laboratory_order(sender, instance, created, **kwargs):
    if created:
        Order.objects.create(
            order_date=instance.order_date,
            order_type=instance.name.name,
            patient=instance.patient,
            doctor=instance.doctor,
             visit=instance.visit,
            added_by=instance.data_recorder,
            cost=instance.cost,
        )

@receiver(post_save, sender=AmbulanceOrder)
def create_ambulance_order(sender, instance, created, **kwargs):
    if created:
        Order.objects.create(
            order_date=instance.order_date,
            order_type='Ambulance',
            patient=instance.patient,
            visit=instance.visit,
            added_by=instance.data_recorder,
            cost=instance.cost,
        )
    