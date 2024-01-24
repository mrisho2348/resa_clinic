from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import BaseUserManager
from django.db.models.signals import post_save,pre_save,post_delete
from django.dispatch import receiver
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone

# Create your models here.
class CustomUserManager(BaseUserManager):
    def create_user(self, username, email, password=None, user_type=1, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, user_type=user_type, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('user_type', 1)  # Set the default user_type for superusers
        return self.create_user(username, email, password, **extra_fields)
    
        
class CustomUser(AbstractUser):
    user_type_data = (
        (1, "AdminHOD"),
        (2, "Staffs"),
    )
    user_type = models.CharField(default=1, choices=user_type_data, max_length=15)
    is_active = models.BooleanField(default=True)

    # Provide unique related_name values
    groups = models.ManyToManyField(
        "auth.Group",
        verbose_name="Groups",
        blank=True,
        help_text="The groups this user belongs to. A user will get all permissions granted to each of their groups.",
        related_name="customuser_groups",  # Add a unique related_name for groups
        related_query_name="user",
    )
    user_permissions = models.ManyToManyField(
        "auth.Permission",
        verbose_name="User permissions",
        blank=True,
        help_text="Specific permissions for this user.",
        related_name="customuser_user_permissions",  # Add a unique related_name for user_permissions
        related_query_name="user",
    )

    objects = CustomUserManager()

    def __str__(self):
        return self.username

class AdminHOD(models.Model):
    id = models.AutoField(primary_key=True)
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='admin_hod')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()

class Staffs(models.Model):
    id = models.AutoField(primary_key=True)
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='staff')   
    middle_name = models.TextField(blank=True)
    gender = models.TextField(max_length=7, blank=True)
    date_of_birth = models.DateField(blank=True, default='2000-01-01')
    phone_number = models.CharField(max_length=14, blank=True)
    marital_status = models.CharField(max_length=20, blank=True)
    profession = models.CharField(max_length=20, blank=True)
    role = models.CharField(max_length=20, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()
    def __str__(self):
        return f"{self.admin.first_name} {self.middle_name} {self.admin.last_name}"

class InsuranceCompany(models.Model):
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=15)
    short_name = models.CharField(max_length=50)
    email = models.EmailField()
    address = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()
    def __str__(self):
        return self.name

class Company(models.Model):
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=50)
    category = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()
    def __str__(self):
        return self.name
    

class Service(models.Model):
    department = models.CharField(max_length=200)
    type_service = models.CharField(max_length=200)
    name = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()

    def __str__(self):
        return self.name
        
class PathodologyRecord(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()
    def __str__(self):
        return self.name
    
    
class DiseaseRecode(models.Model):
    disease_name = models.CharField(max_length=255)
    code = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()
    def __str__(self):
        return self.name
  
class ContactDetails(models.Model):    
    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    subject = models.CharField(max_length=255)
    message = models.TextField()
    subscribe_newsletter = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()
    def __str__(self):
        return self.name
    



class Patients(models.Model):
    # Auto-incremented primary key (ID)
    # The unique constraint for MRN is maintained separately
    mrn = models.CharField(max_length=20, unique=True, editable=False)
    fullname = models.CharField(max_length=255)
    email = models.EmailField()
    dob = models.DateField()
    gender = models.CharField(max_length=255)
    phone = models.CharField(max_length=15)
    address = models.TextField()
    nationality = models.CharField(max_length=255)
    company = models.CharField(max_length=255)
    marital_status = models.CharField(max_length=255)
    patient_type = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()

    def save(self, *args, **kwargs):
        # Generate MRN only if it's not provided
        if not self.mrn:
            self.mrn = generate_mrn()

        super().save(*args, **kwargs)

    def __str__(self):
        return self.fullname

def generate_mrn():
    # Retrieve the last patient's MRN from the database
    last_patient = Patients.objects.last()

    # Extract the numeric part from the last MRN, or start from 0 if there are no patients yet
    last_mrn_number = int(last_patient.mrn.split('-')[-1]) if last_patient else 0

    # Increment the numeric part for the new patient
    new_mrn_number = last_mrn_number + 1

    # Format the MRN with leading zeros and concatenate with the prefix "PAT-"
    new_mrn = f"PAT-{new_mrn_number:05d}"

    return new_mrn
    
    
class Payment(models.Model):
    PAYMENT_TYPES = [
        ('Cash', 'Cash'),
        ('Credit Card', 'Credit Card'),
        ('Insurance', 'Insurance'),
        # Add more payment types as needed
    ]

    payment_type = models.CharField(max_length=20, choices=PAYMENT_TYPES)
    patient_id = models.ForeignKey(Patients, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date_paid = models.DateField()
    insurance_id = models.ForeignKey(InsuranceCompany, on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return f"Payment of {self.amount} {self.payment_type} for {self.patient_id}"

class Procedure(models.Model):
    patient = models.ForeignKey(Patients, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField()
    duration_time = models.CharField(max_length=50)
    equipments_used = models.CharField(max_length=255)
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()

    def __str__(self):
        return f"Procedure: {self.name} for {self.patient_id}"
class Consultation(models.Model):
    doctor = models.ForeignKey(Staffs, on_delete=models.CASCADE)
    patient = models.ForeignKey(Patients, on_delete=models.CASCADE)
    appointment_date = models.DateField()
    start_time = models.TimeField(blank=True, null=True)
    end_time = models.TimeField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    STATUS_CHOICES = [
    (0, 'Pending'),
    (1, 'Completed'),
    (2, 'Canceled'),
    (3, 'Rescheduled'),
    (4, 'No-show'),
    (5, 'In Progress'),
    (6, 'Confirmed'),
    (7, 'Arrived'),
   
]
    status = models.IntegerField(choices=STATUS_CHOICES, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()
    def __str__(self):
        return f"Appointment with {self.doctor.name} for {self.patient.name} on {self.appointment_date} from {self.start_time} to {self.end_time}"

class Notification(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)    
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()
   
class NotificationMedicine(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    is_read = models.BooleanField(default=False)    
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()
    def __str__(self):
        return f"{self.user.username} - {self.message}"   

MEDICINE_TYPES = [
    ('Tablet', 'Tablet'),
    ('Capsule', 'Capsule'),
    ('Syrup', 'Syrup'),
    ('Injection', 'Injection'),
    ('Ointment', 'Ointment'),
    ('Drops', 'Drops'),
    ('Inhaler', 'Inhaler'),
    ('Patch', 'Patch'),
    ('Liquid', 'Liquid'),
    ('Cream', 'Cream'),
    ('Gel', 'Gel'),
    ('Suppository', 'Suppository'),
    ('Powder', 'Powder'),
    ('Lotion', 'Lotion'),
    ('Suspension', 'Suspension'),
    ('Lozenge', 'Lozenge'),
    # Add more medicine types as needed
]

class Medicine(models.Model):
    name = models.CharField(max_length=100)
    medicine_type = models.CharField(max_length=20, choices=MEDICINE_TYPES)
    side_effect = models.TextField(blank=True, null=True)
    dosage = models.CharField(max_length=50)
    storage_condition = models.CharField(max_length=100)
    manufacturer = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    expiration_date = models.DateField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    transactions = models.ManyToManyField('Transaction', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()
    def __str__(self):
        return self.name    
    
class Transaction(models.Model):
    date = models.DateField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    # Medicines associated with this transaction through the MedicineTransaction model
    medicines = models.ManyToManyField(Medicine, through='MedicineTransaction')
    # Additional fields for Transaction
    payment_method = models.CharField(max_length=20, choices=[('Cash', 'Cash'), ('Credit Card', 'Credit Card')])
    is_successful = models.BooleanField(default=False)
    transaction_status = models.CharField(max_length=20, choices=[('Pending', 'Pending'), ('Completed', 'Completed')])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()
    def __str__(self):
        return f"Transaction #{self.id} on {self.date} for {self.amount} ({'Successful' if self.is_successful else 'Pending'})"
    
class MedicineInventory(models.Model):
    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    purchase_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()
    
    def __str__(self):
        return f"{self.medicine.medicine_name} - Quantity: {self.quantity}" 
    

class MedicineTransaction(models.Model):
    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE)
    transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    total_cost = models.DecimalField(max_digits=10, decimal_places=2)  
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()     
class MedicalRecordConsultation(models.Model):
    # Relationship with Patient
    patient = models.ForeignKey(Patients, on_delete=models.CASCADE)
    # Complaints Section
    chief_complaint = models.CharField(max_length=255)
    history_illness = models.TextField()
    physical_examination = models.TextField()
    # Allergy to Medications
    allergy_medications = models.TextField()
    # Diagnosis Section
    provisional_diagnosis = models.TextField()
    final_diagnosis = models.TextField()
    # Pathology, Plan, and Injury
    pathology = models.ForeignKey(PathodologyRecord, on_delete=models.CASCADE)
    plan = models.TextField()
    # Fatality, Injury Description, and Disposition
    injury = models.CharField(max_length=200)
    fatality = models.CharField(max_length=200)
    injury_description = models.TextField()
    # Disposition Section
    disposition =  models.CharField(max_length=200)
    destination = models.CharField(max_length=255)
    disposition_description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()
    def __str__(self):
        return f"{self.patient.name}'s Medical Record"  
    
      
    
@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        if instance.user_type == 1:  # HOD
            AdminHOD.objects.create(admin=instance)
        elif instance.user_type == 2:  # Staff
            Staffs.objects.create(admin=instance)

@receiver(post_save, sender=CustomUser)
def save_user_profile(sender, instance, **kwargs):
    if instance.user_type == 1:
        instance.admin_hod.save()
    elif instance.user_type == 2:
        instance.staff.save()
