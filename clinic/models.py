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
    cost = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)  # New field for cost
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()

    def __str__(self):
        return self.name

        
class PathodologyRecord(models.Model):
    name = models.CharField(max_length=255)
    related_diseases = models.ManyToManyField('DiseaseRecode', blank=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()
    def __str__(self):
        return self.name
    
    
class DiseaseRecode(models.Model):
    disease_name = models.CharField(max_length=255)
    related_pathology_records = models.ManyToManyField(PathodologyRecord, blank=True)
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
    patient = models.ForeignKey(Patients, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date_paid = models.DateField()
    insurance = models.ForeignKey(InsuranceCompany, on_delete=models.SET_NULL, blank=True, null=True)
    def __str__(self):
        return f"Payment of {self.amount} {self.payment_type} for {self.patient}"

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
        return f"Procedure: {self.name} for {self.patient}"
    
class ConsultationFee(models.Model):
    doctor = models.ForeignKey(Staffs, on_delete=models.CASCADE)
    patient = models.ForeignKey(Patients, on_delete=models.CASCADE)
    fee_amount = models.DecimalField(max_digits=10, decimal_places=2)    
    consultation = models.ForeignKey('Consultation', on_delete=models.SET_NULL, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()
    def __str__(self):
        return f"Consultation fee of {self.fee_amount} for {self.doctor.name} by {self.patient.fullname} on {self.consultation_date}"
    
    
class DiagnosticTest(models.Model):
    # Unique identifier for DiagnosticTest
    test_id = models.CharField(max_length=12, unique=True, editable=False)
    patient = models.ForeignKey('Patients', on_delete=models.CASCADE, related_name='diagnostic_tests')
    test_type = models.CharField(max_length=255)
    test_date = models.DateField()
    result = models.TextField(blank=True, null=True)
    # Additional Fields for Diseases
    diseases = models.ManyToManyField(DiseaseRecode)
    health_issues = models.ManyToManyField('HealthIssue')
    pathology_record = models.ForeignKey(PathodologyRecord, on_delete=models.SET_NULL, blank=True, null=True)
    def save(self, *args, **kwargs):
        # Generate a unique identifier based on count of existing records
        if not self.test_id:
            self.test_id = generate_test_id()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.test_type} for {self.patient.fullname} on {self.test_date}"

def generate_test_id():
    # Retrieve the last diagnostic test from the database
    last_test = DiagnosticTest.objects.last()

    # Extract the numeric part from the last TID, or start from 0 if there are no tests yet
    last_test_number = int(last_test.test_id.split('-')[-1]) if last_test else 0

    # Increment the numeric part for the new test
    new_test_number = last_test_number + 1

    # Format the TID with leading zeros and concatenate with the prefix "TID-"
    new_test_id = f"TID-{new_test_number:05d}"

    return new_test_id
      
class Sample(models.Model):
    sample_id = models.CharField(max_length=12, unique=True, editable=False)
    lab_test = models.ForeignKey(DiagnosticTest, on_delete=models.CASCADE, related_name='samples')
    collection_date = models.DateField(null=True, blank=True)
    processing_date = models.DateField(null=True, blank=True)
    analysis_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=[('collected', 'Collected'), ('processing', 'Processing'), ('analyzed', 'Analyzed')], default='collected')


    def save(self, *args, **kwargs):
        # Generate a unique identifier based on count of existing records
        if not self.sample_id:
            self.sample_id = generate_sample_id()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Sample {self.sample_id} - {self.lab_test.test_type} - {self.status}"

def generate_sample_id():
    last_sample = Sample.objects.last()
    last_sample_number = int(last_sample.sample_id.split('-')[-1]) if last_sample else 0
    new_sample_number = last_sample_number + 1
    return f"SMP-{new_sample_number:05d}"    
    
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
    pathodology_record = models.ForeignKey(PathodologyRecord, on_delete=models.SET_NULL, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()    
    
    def __str__(self):
        return f"Appointment with {self.doctor.admin.first_name} {self.doctor.middle_name} {self.doctor.admin.last_name} for {self.patient.fullname} on {self.appointment_date} from {self.start_time} to {self.end_time}"
    
    def save(self, *args, **kwargs):
        # Set a default pathodology record if none is provided
        if not self.pathodology_record:
            default_pathodology = PathodologyRecord.objects.get_or_create(name="Default Pathodology")[0]
            self.pathodology_record = default_pathodology

        super().save(*args, **kwargs)

    

class Notification(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)    
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()
    
class Referral(models.Model):
    # Patient who is being referred
    patient = models.ForeignKey(Patients, on_delete=models.CASCADE)
    # Information about the referral
    source_location  = models.CharField(max_length=255, help_text='Source location of the patient')
    destination_location = models.CharField(max_length=255, help_text='Destination location for MedEvac')
    reason = models.TextField()
    # Additional details
    referral_date = models.DateField(auto_now_add=True, help_text='Date when the referral was made')
    # Status of the referral (e.g., pending, accepted, rejected)
    REFERRAL_STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    )
    status = models.CharField(max_length=20, choices=REFERRAL_STATUS_CHOICES, default='pending')
    # Additional fields as needed
    notes = models.TextField(blank=True, null=True, help_text='Additional notes about the referral')
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()

    def __str__(self):
        return f"Referral for {self.patient} to {self.destination_location} at {self.source_location} on {self.referral_date}"   
    
    def get_status_class(self):
        if self.status == 'pending':
            return 'text-warning'
        elif self.status == 'accepted':
            return 'text-success'
        elif self.status == 'rejected':
            return 'text-danger'
        return ''

    def get_status_color(self):
        if self.status == 'pending':
            return 'warning'
        elif self.status == 'accepted':
            return 'success'
        elif self.status == 'rejected':
            return 'danger'
        return '' 
   
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
    medicine = models.ForeignKey('Medicine', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    purchase_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()

    def __str__(self):
        return f"{self.medicine.name} - Quantity: {self.quantity}"

    @classmethod
    def update_or_create_inventory(cls, medicine_id, quantity, purchase_date):
        existing_record = cls.objects.filter(medicine_id=medicine_id).first()

        if existing_record:
            # Update the existing record's quantity
            existing_record.quantity += quantity
            existing_record.save()
        else:
            # Create a new record
            cls.objects.create(
                medicine_id=medicine_id,
                quantity=quantity,
                purchase_date=purchase_date
            )
    
# Now, the additional model
class PathologyDiagnosticTest(models.Model):
    pathology_record = models.ForeignKey(PathodologyRecord, on_delete=models.CASCADE, related_name='diagnostic_tests')
    diagnostic_test = models.ForeignKey(DiagnosticTest, on_delete=models.CASCADE)
    
    # Additional fields
    test_result = models.TextField(blank=True, null=True)
    testing_date = models.DateField(blank=True, null=True)
    conducted_by = models.CharField(max_length=255, blank=True, null=True)
    def __str__(self):
        return f"{self.pathology_record.name} - {self.diagnostic_test.test_type}"    
class MedicationPayment(models.Model):
    patient = models.ForeignKey(Patients, on_delete=models.CASCADE, null=True, blank=True)
    non_registered_patient_name = models.CharField(max_length=255, null=True, blank=True)
    non_registered_patient_email = models.EmailField(null=True, blank=True)
    non_registered_patient_phone = models.CharField(max_length=15, null=True, blank=True)
    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateField()

    def __str__(self):
        patient_info = self.patient.fullname if self.patient else f"Non-Registered: {self.non_registered_patient_name}"
        return f"Payment of {self.amount} for {self.quantity} {self.medicine.name}(s) by {patient_info} on {self.payment_date}"

    
    



class MedicineTransaction(models.Model):
    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE)
    transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    total_cost = models.DecimalField(max_digits=10, decimal_places=2)  
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()     
    
class PatientDisease(models.Model):
    patient = models.ForeignKey(Patients, on_delete=models.CASCADE, related_name='diseases')
    disease_record = models.ForeignKey(DiseaseRecode, on_delete=models.CASCADE)    
    # Additional fields related to the patient's diagnosis
    diagnosis_date = models.DateField()
    severity = models.CharField(max_length=50)
    treatment_plan = models.TextField(blank=True, null=True)
    # Add more fields as needed    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()

    def __str__(self):
        return f"{self.patient.fullname} - {self.disease_record.disease_name} ({self.diagnosis_date})"
    
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
    
   
class HealthIssue(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    is_disease = models.BooleanField(default=True)
    
    # Additional fields
    severity = models.CharField(max_length=50, blank=True, null=True)
    treatment_plan = models.TextField(blank=True, null=True)
    onset_date = models.DateField(blank=True, null=True)
    resolution_date = models.DateField(blank=True, null=True)
    # Add more fields as needed
    
    def __str__(self):
        return self.name
      
    
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
