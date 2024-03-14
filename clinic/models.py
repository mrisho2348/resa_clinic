from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import BaseUserManager
from django.db.models.signals import post_save,pre_save,post_delete
from django.dispatch import receiver
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
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
    
class LabTest(models.Model):
    patient = models.ForeignKey('RemotePatient', on_delete=models.CASCADE)
    visit = models.ForeignKey('RemotePatientVisits', on_delete=models.CASCADE)
    consultation = models.ForeignKey('RemoteConsultationNotes', on_delete=models.CASCADE)
    diagnosis = models.ForeignKey('Diagnosis', on_delete=models.CASCADE,blank=True, null=True)
    test_name = models.CharField(max_length=100, verbose_name=_('Test Name'))
    result = models.TextField(blank=True, verbose_name=_('Test Result'))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    lab_number = models.CharField(max_length=20, unique=True, verbose_name=_('Lab Number'))

    def save(self, *args, **kwargs):
        if not self.lab_number:
            last_lab_test = LabTest.objects.order_by('-id').first()
            if last_lab_test:
                last_lab_number = int(last_lab_test.lab_number.split('-')[-1])
                new_lab_number = f"LAB-{last_lab_number + 1:07d}"
            else:
                new_lab_number = "LAB-0000001"
            self.lab_number = new_lab_number
        super().save(*args, **kwargs)

    objects = models.Manager()
    # Add more fields as needed
    

class RemoteCompany(models.Model):
    name = models.CharField(max_length=255)
    industry = models.CharField(max_length=50, default="Unspecified", null=True)
    sector = models.CharField(max_length=50, default="Unspecified", null=True)
    headquarters = models.CharField(max_length=100, default="Unspecified", null=True)
    Founded = models.CharField(max_length=10,null=True, default="Unspecified",)
    Notes = models.TextField(max_length=100, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()

    def __str__(self):
        return self.name
    
class PatientMedicationAllergy(models.Model):
    patient = models.ForeignKey('RemotePatient', on_delete=models.CASCADE, related_name='medication_allergies')
    medicine_name = models.CharField(max_length=100)
    reaction = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.medicine_name} - {self.reaction}"
    
class PatientSurgery(models.Model):
    patient = models.ForeignKey('RemotePatient', on_delete=models.CASCADE)
    surgery_name = models.CharField(max_length=100,blank=True, null=True)
    surgery_date = models.DateField(blank=True, null=True)   
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()
    def __str__(self):
        return f"{self.surgery_name} - {self.surgery_date}"  
    
class PatientLifestyleBehavior(models.Model):
    patient = models.ForeignKey('RemotePatient', on_delete=models.CASCADE)
    weekly_exercise_frequency = models.CharField(max_length=100)    
    smoking = models.BooleanField(default=False)
    alcohol_consumption = models.BooleanField(default=False)    
    healthy_diet = models.BooleanField(default=False)
    stress_management = models.BooleanField(default=False)
    sufficient_sleep = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.patient} - {self.behavior_name}"

class Service(models.Model):
    coverage = models.CharField(max_length=200, blank=True, null=True)
    department = models.CharField(max_length=200, blank=True, null=True)
    type_service = models.CharField(max_length=200, blank=True, null=True)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    cost = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)  # New field for cost
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()

    def __str__(self):
        return self.name

class InventoryItem(models.Model):
    name = models.CharField(max_length=100)
    quantity = models.PositiveIntegerField()
    category = models.ForeignKey('Category', on_delete=models.SET_NULL, null=True, blank=True)
    description = models.TextField(blank=True)    
    supplier = models.ForeignKey('Supplier', on_delete=models.SET_NULL, null=True, blank=True)
    purchase_date = models.DateField(null=True, blank=True)
    purchase_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    expiry_date = models.DateField(null=True, blank=True)
    location_in_storage = models.CharField(max_length=100, blank=True)
    min_stock_level = models.PositiveIntegerField(null=True, blank=True)
    images_attachments = models.ImageField(upload_to='inventory/images/', null=True, blank=True)
    condition = models.CharField(max_length=50, blank=True)
    remain_quantity = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()
    


    def __str__(self):
        return self.name  
   
class UsageHistory(models.Model):
    inventory_item = models.ForeignKey(InventoryItem, on_delete=models.CASCADE)
    usage_date = models.DateField()
    quantity_used = models.PositiveIntegerField()
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()
    
    def __str__(self):
        return f"{self.usage_date} - {self.quantity_used} units"    
class Category(models.Model):
    name = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()

    def __str__(self):
        return self.name    
        
class Supplier(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=100,blank=True, null=True)
    contact_information = models.TextField(blank=True)
    email = models.EmailField(max_length=255, blank=True, null=True)
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
    first_name = models.CharField(max_length=100, blank=True, null=True)
    middle_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    gender = models.CharField(max_length=10, choices=[('Male', 'Male'), ('Female', 'Female')])
    age = models.IntegerField(blank=True, null=True)
    dob = models.DateField(null=True, blank=True) 
    phone = models.CharField(max_length=15)
    address = models.TextField()
    nationality = models.ForeignKey('Country', on_delete=models.CASCADE) 
     # New payment-related fields
    PAYMENT_CHOICES = [
        ('cash', 'Cash'),
        ('insurance', 'Insurance'),
    ]
    payment_form = models.CharField(max_length=255, choices=PAYMENT_CHOICES)
    insurance_name = models.CharField(max_length=255, blank=True, null=True)
    insurance_number = models.CharField(max_length=255, blank=True, null=True)
    emergency_contact_name = models.CharField(max_length=100, blank=True, null=True)
    emergency_contact_relation = models.CharField(max_length=100, blank=True, null=True)    
    emergency_contact_phone = models.CharField(max_length=20, blank=True, null=True)
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
        return self.last_name



    
def generate_mrn():
    # Retrieve the last patient's MRN from the database
    last_patient = Patients.objects.last()

    # Extract the numeric part from the last MRN, or start from 0 if there are no patients yet
    last_mrn_number = int(last_patient.mrn.split('-')[-1]) if last_patient else 0

    # Increment the numeric part for the new patient
    new_mrn_number = last_mrn_number + 1

    # Format the MRN with leading zeros and concatenate with the prefix "PAT-"
    new_mrn = f"RES-{new_mrn_number:07d}"

    return new_mrn

def generate_for_remote_mrn():
    # Retrieve the last patient's MRN from the database
    last_patient = RemotePatient.objects.last()

    # Extract the numeric part from the last MRN, or start from 0 if there are no patients yet
    last_mrn_number = int(last_patient.mrn.split('-')[-1]) if last_patient else 0

    # Increment the numeric part for the new patient
    new_mrn_number = last_mrn_number + 1

    # Format the MRN with leading zeros and concatenate with the prefix "PAT-"
    new_mrn = f"PAT-{new_mrn_number:05d}"

    return new_mrn
    


class RemotePatient(models.Model):
    mrn = models.CharField(max_length=20, unique=True, editable=False, verbose_name='MRN')
    first_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    gender = models.CharField(max_length=10, choices=[('Male', 'Male'), ('Female', 'Female')])
    age = models.IntegerField(blank=True, null=True)
    dob = models.DateField(null=True, blank=True)
    nationality = models.ForeignKey('Country', on_delete=models.CASCADE) 
    phone = models.CharField(max_length=20)
    osha_certificate = models.BooleanField(default=False)
    date_of_osha_certification = models.DateField(null=True, blank=True)
    insurance = models.CharField(max_length=20, choices=[('Uninsured', 'Uninsured'), ('Insured', 'Insured'), ('Unknown', 'Unknown')])
    insurance_company = models.CharField(max_length=100, blank=True, null=True)
    other_insurance_company = models.CharField(max_length=100, blank=True, null=True)
    insurance_number = models.CharField(max_length=100, blank=True, null=True)
    emergency_contact_name = models.CharField(max_length=100)
    emergency_contact_relation = models.CharField(max_length=100, blank=True, null=True)
    other_emergency_contact_relation = models.CharField(max_length=100,blank=True, null=True)
    emergency_contact_phone = models.CharField(max_length=20)
    marital_status = models.CharField(max_length=20, choices=[('Single', 'Single'), ('Married', 'Married'), ('Divorced', 'Divorced'), ('Widowed', 'Widowed')],default="Single")
    occupation = models.CharField(max_length=100, blank=True, null=True)
    other_occupation = models.CharField(max_length=100, blank=True, null=True)
    patient_type = models.CharField(max_length=100, blank=True, null=True)
    other_patient_type = models.CharField(max_length=100, blank=True, null=True)
    company = models.ForeignKey(RemoteCompany, on_delete=models.CASCADE)    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created At')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Updated At')
    objects = models.Manager()
    
    def save(self, *args, **kwargs):
        # Generate MRN only if it's not provided
        if not self.mrn:
            self.mrn = generate_for_remote_mrn()

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"   


   

    
    
class PatientHealthCondition(models.Model):
    patient = models.ForeignKey(RemotePatient, on_delete=models.CASCADE, related_name='health_conditions', verbose_name='Patient')    
    health_condition = models.CharField(max_length=200, blank=True, null=True, verbose_name='Health Condition')
    health_condition_notes = models.CharField(max_length=200, blank=True, null=True, verbose_name='Health Condition Notes')  
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created At')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Updated At')
    
    objects = models.Manager()  

class FamilyMedicalHistory(models.Model):
    patient = models.ForeignKey(RemotePatient, on_delete=models.CASCADE, related_name='family_medical_history', verbose_name='Patient')
    condition = models.CharField(max_length=100, verbose_name='Condition')
    relationship = models.CharField(max_length=100, blank=True, null=True, verbose_name='Relationship')
    comments = models.CharField(max_length=100, blank=True, null=True, verbose_name='Comments')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created At')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Updated At')

    objects = models.Manager()

    def __str__(self):
        return f"{self.patient} - {self.condition}"
            
class RemoteService(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2) 
    description = models.TextField( null=True, blank=True,)
    category = models.CharField(max_length=50, null=True, blank=True,)   
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()        
    
    def __str__(self):
        return f"{self.name}-{self.category}"
    
    
class Country(models.Model):
        name = models.CharField(max_length=100)
        created_at = models.DateTimeField(auto_now_add=True)
        updated_at = models.DateTimeField(auto_now=True)
        objects = models.Manager()        
    
        def __str__(self):
            return f"{self.name}"    
    
class ServiceRequest(models.Model):
    STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
    )

    patient = models.ForeignKey(RemotePatient, on_delete=models.CASCADE)
    visit = models.ForeignKey('RemotePatientVisits', on_delete=models.CASCADE)
    service = models.ForeignKey(RemoteService, on_delete=models.CASCADE)
    date_requested = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    result = models.TextField(blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()

    def __str__(self):
        return f"{self.patient} - {self.service} ({self.status})"    
class PatientVital(models.Model):
    patient = models.ForeignKey('Patients', on_delete=models.CASCADE)
    visit = models.ForeignKey('PatientVisits', on_delete=models.CASCADE,blank=True, null=True) 
    recorded_by = models.ForeignKey(Staffs, on_delete=models.CASCADE,blank=True, null=True) 
    recorded_at = models.DateTimeField(auto_now_add=True)
    respiratory_rate = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, help_text="Respiratory rate in breaths per minute")
    pulse_rate = models.PositiveIntegerField(null=True, blank=True, help_text="Pulse rate in beats per minute")
    blood_pressure = models.CharField(max_length=20, null=True, blank=True, help_text="Blood pressure measurement")
    spo2 = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, help_text="SPO2 measurement in percentage")
    temperature = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, help_text="Temperature measurement in Celsius")
    gcs = models.PositiveIntegerField(null=True, blank=True, help_text="Glasgow Coma Scale measurement")
    avpu = models.CharField(max_length=20, null=True, blank=True, help_text="AVPU scale measurement")
    weight = models.CharField(max_length=20, null=True, blank=True, help_text="weight")
    unique_identifier = models.CharField(max_length=20, unique=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()

    def __str__(self):
        return f"Vital information for {self.patient} recorded at {self.recorded_at}"

    def save(self, *args, **kwargs):
        # Generate a unique identifier based on the patient's format
        if not self.unique_identifier:
            self.unique_identifier = self.generate_unique_identifier()
        super().save(*args, **kwargs)

    def generate_unique_identifier(self):
        last_patient_vital = PatientVital.objects.last()
        last_number = int(last_patient_vital.unique_identifier.split('-')[-1]) if last_patient_vital else 0
        new_number = last_number + 1
        return f"VTN-{new_number:07d}"
    
class RemotePatientVital(models.Model):
    patient = models.ForeignKey('RemotePatient', on_delete=models.CASCADE)
    visit = models.ForeignKey('RemotePatientVisits', on_delete=models.CASCADE)  
    recorded_at = models.DateTimeField(auto_now_add=True)
    respiratory_rate = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, help_text="Respiratory rate in breaths per minute")
    pulse_rate = models.PositiveIntegerField(null=True, blank=True, help_text="Pulse rate in beats per minute")
    blood_pressure = models.CharField(max_length=20, null=True, blank=True, help_text="Blood pressure measurement")
    spo2 = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, help_text="SPO2 measurement in percentage")
    temperature = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, help_text="Temperature measurement in Celsius")
    gcs = models.PositiveIntegerField(null=True, blank=True, help_text="Glasgow Coma Scale measurement")
    avpu = models.CharField(max_length=20, null=True, blank=True, help_text="AVPU scale measurement")
    unique_identifier = models.CharField(max_length=20, unique=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()

    def __str__(self):
        return f"Vital information for {self.patient} recorded at {self.recorded_at}"

    def save(self, *args, **kwargs):
        # Generate a unique identifier based on the patient's format
        if not self.unique_identifier:
            self.unique_identifier = self.generate_remoteunique_identifier()
        super().save(*args, **kwargs)

    def generate_remoteunique_identifier(self):
        last_patient_vital = RemotePatientVital.objects.last()
        last_number = int(last_patient_vital.unique_identifier.split('-')[-1]) if last_patient_vital else 0
        new_number = last_number + 1
        return f"VTN-{new_number:07d}"

        
class PatientVisits(models.Model):
    VISIT_TYPES = (
        ('Normal', _('Normal')),
        ('Emergency', _('Emergency')),
        ('Referral', _('Referral')),
        ('Follow up', _('Follow up')),
    )

    patient = models.ForeignKey('Patients', on_delete=models.CASCADE)
    vst = models.CharField(max_length=20, unique=True, editable=False)
    visit_type = models.CharField( max_length=15, choices=VISIT_TYPES)
    visit_reason = models.TextField(blank=True, null=True)
    referral_number = models.CharField(max_length=50, blank=True, null=True)
    primary_service = models.CharField(max_length=50)
    insurance_number = models.CharField(max_length=50, blank=True, null=True)
    insurance_name = models.CharField(max_length=50, blank=True, null=True)
    payment_scheme = models.CharField(max_length=50, blank=True, null=True)
    authorization_code = models.CharField(max_length=50, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('Visit')
        verbose_name_plural = _('Visits')
        
    def save(self, *args, **kwargs):
        # Generate MRN only if it's not provided
        if not self.vst:
            self.vst = generate_vst()

        super().save(*args, **kwargs)   

    def __str__(self):
        return f'{self.patient} - {self.get_visit_type_display()}'
    
def generate_vst():
    # Retrieve the last patient's VST from the database
    last_patient_visit = PatientVisits.objects.last()

    # Extract the numeric part from the last VST, or start from 0 if there are no patients yet
    last_vst_number = int(last_patient_visit.vst.split('-')[-1]) if last_patient_visit else 0

    # Increment the numeric part for the new patient
    new_vst_number = last_vst_number + 1

    # Format the VST with leading zeros and concatenate with the prefix "PAT-"
    new_vst = f"VST-{new_vst_number:07d}"

    return new_vst  


class Diagnosis(models.Model):
    diagnosis_name= models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()
    
    def __str__(self):
        return self.diagnosis_name
    
    

class ConsultationNotes(models.Model):
    doctor = models.ForeignKey(Staffs, on_delete=models.CASCADE)
    patient = models.ForeignKey(Patients, on_delete=models.CASCADE)
    visit = models.ForeignKey(PatientVisits, on_delete=models.CASCADE,blank=True, null=True) 
    chief_complaints = models.TextField(null=True, blank=True)
    history_of_presenting_illness = models.TextField(null=True, blank=True)
    consultation_number = models.CharField(max_length=20, unique=True)
    physical_examination = models.TextField(null=True, blank=True)
    allergy_to_medications = models.CharField(max_length=255, null=True, blank=True)
    provisional_diagnosis = models.ManyToManyField(Diagnosis, related_name='provisional_diagnosis_notes', blank=True)
    final_diagnosis = models.ManyToManyField(Diagnosis, related_name='final_diagnosis_notes', blank=True)
    pathology = models.ManyToManyField(PathodologyRecord, blank=True)
    doctor_plan = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()

    def __str__(self):
        return f"Consultation for {self.patient} by Dr. {self.doctor}"
    
    def save(self, *args, **kwargs):
        if not self.consultation_number:
            self.consultation_number = generate_consultation_number()
        super().save(*args, **kwargs)   
    
def generate_consultation_number():
    last_consultation_notes = ConsultationNotes.objects.last()
    last_sample_number = int(last_consultation_notes.consultation_number.split('-')[-1]) if last_consultation_notes else 0
    new_consultation_number = last_sample_number + 1
    return f"CTN-{new_consultation_number:07d}"    
   
class RemoteConsultationNotes(models.Model):
    doctor = models.ForeignKey(Staffs, on_delete=models.CASCADE)
    patient = models.ForeignKey(RemotePatient, on_delete=models.CASCADE)
    visit = models.ForeignKey('RemotePatientVisits', on_delete=models.CASCADE)  
    chief_complaints = models.TextField(null=True, blank=True)
    history_of_presenting_illness = models.TextField(null=True, blank=True)
    consultation_number = models.CharField(max_length=20, unique=True)
    physical_examination = models.TextField(null=True, blank=True)
    allergy_to_medications = models.CharField(max_length=255, null=True, blank=True)
    provisional_diagnosis = models.ManyToManyField(Diagnosis, related_name='provisional_notes', blank=True)
    final_diagnosis = models.ManyToManyField(Diagnosis, related_name='final_notes', blank=True)
    pathology = models.ManyToManyField(PathodologyRecord, blank=True)
    doctor_plan = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()

    def __str__(self):
        return f"Consultation for {self.patient} by Dr. {self.doctor}"
    
    def save(self, *args, **kwargs):
        if not self.consultation_number:
            self.consultation_number = generate_remoteconsultation_number()
        super().save(*args, **kwargs)   
    
def generate_remoteconsultation_number():
    last_consultation_notes = RemoteConsultationNotes.objects.last()
    last_sample_number = int(last_consultation_notes.consultation_number.split('-')[-1]) if last_consultation_notes else 0
    new_consultation_number = last_sample_number + 1
    return f"CTN-{new_consultation_number:07d}"       
  
class RemotePatientVisits(models.Model):
    VISIT_TYPES = (
        ('Normal', _('Normal')),
        ('Emergency', _('Emergency')),
        ('Referral', _('Referral')),
        ('Follow up', _('Follow up')),
    )

    patient = models.ForeignKey('RemotePatient', on_delete=models.CASCADE)
    vst = models.CharField(max_length=20, unique=True, editable=False)
    visit_type = models.CharField( max_length=15, choices=VISIT_TYPES)     
    primary_service = models.CharField(max_length=50) 
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('Visit')
        verbose_name_plural = _('Visits')
        
    def save(self, *args, **kwargs):
        # Generate MRN only if it's not provided
        if not self.vst:
            self.vst = remotegenerate_vst()

        super().save(*args, **kwargs)   

    def __str__(self):
        return f'{self.patient} - {self.get_visit_type_display()}'
    
def remotegenerate_vst():
    # Retrieve the last patient's VST from the database
    last_patient_visit = RemotePatientVisits.objects.last()

    # Extract the numeric part from the last VST, or start from 0 if there are no patients yet
    last_vst_number = int(last_patient_visit.vst.split('-')[-1]) if last_patient_visit else 0

    # Increment the numeric part for the new patient
    new_vst_number = last_vst_number + 1

    # Format the VST with leading zeros and concatenate with the prefix "PAT-"
    new_vst = f"VST-{new_vst_number:07d}"

    return new_vst    
        
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

class ImagingRecord(models.Model):
    patient = models.ForeignKey('Patients', on_delete=models.CASCADE)
    visit = models.ForeignKey('PatientVisits', on_delete=models.CASCADE)
    doctor = models.ForeignKey(Staffs, on_delete=models.CASCADE,blank=True, null=True) 
    imaging= models.ForeignKey(Service, on_delete=models.CASCADE,blank=True, null=True) 
    order_date = models.DateField(null=True, blank=True)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='imaging_records/', null=True, blank=True)
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()

    def __str__(self):
        return f"Imaging Record for {self.patient} - {self.imaging_type} ({self.imaging_date})"

class Procedure(models.Model):
    patient = models.ForeignKey(Patients, on_delete=models.CASCADE)
    visit = models.ForeignKey(PatientVisits, on_delete=models.CASCADE,blank=True, null=True) 
    doctor = models.ForeignKey(Staffs, on_delete=models.CASCADE,blank=True, null=True) 
    name = models.ForeignKey(Service, on_delete=models.CASCADE,blank=True, null=True) 
    description = models.TextField(blank=True, null=True)  
    order_date = models.DateField(null=True, blank=True)     
    equipments_used = models.CharField(max_length=255)
    procedure_number = models.CharField(max_length=20, unique=True)  # Unique procedure number
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()

    def __str__(self):
        return f"Procedure: {self.name} for {self.patient}"
    
    def save(self, *args, **kwargs):  
        
        # Generate and set the appointment number if it's not already set
        if not self.procedure_number:
            last_procedure = Procedure.objects.order_by('-id').first()  # Get the last appointment
            if last_procedure:
                last_number = int(last_procedure.procedure_number.split('-')[-1])
            else:
                last_number = 0
            new_number = last_number + 1
            self.procedure_number = f"PR-{new_number:07}"  # Format the appointment number
        super().save(*args, **kwargs)  # Call the original save method
class LaboratoryOrder(models.Model):
    patient = models.ForeignKey(Patients, on_delete=models.CASCADE)
    visit = models.ForeignKey(PatientVisits, on_delete=models.CASCADE,blank=True, null=True) 
    doctor = models.ForeignKey(Staffs, on_delete=models.CASCADE,blank=True, null=True) 
    name = models.ForeignKey(Service, on_delete=models.CASCADE,blank=True, null=True) 
    description = models.TextField(blank=True, null=True)  
    order_date = models.DateField(null=True, blank=True)  
    result = models.TextField(blank=True, verbose_name=_('Test Result'))
    lab_number = models.CharField(max_length=20, unique=True)  # Unique procedure number
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()

    def __str__(self):
        return f"LaboratoryOrder: {self.name} for {self.patient}"
    
    def save(self, *args, **kwargs):  
        
        # Generate and set the appointment number if it's not already set
        if not self.lab_number:
            last_lab_number = LaboratoryOrder.objects.order_by('-id').first()  # Get the last appointment
            if last_lab_number:
                last_number = int(last_lab_number.lab_number.split('-')[-1])
            else:
                last_number = 0
            new_number = last_number + 1
            self.lab_number = f"LAB-{new_number:07}"  # Format the appointment number
        super().save(*args, **kwargs)  # Call the original save method
        
        
class AmbulanceOrder(models.Model):
    patient = models.ForeignKey(Patients, on_delete=models.CASCADE)
    visit = models.ForeignKey(PatientVisits, on_delete=models.CASCADE, blank=True, null=True) 
    service = models.CharField(max_length=100)
    from_location = models.CharField(max_length=100)
    to_location = models.CharField(max_length=100)
    age = models.CharField(max_length=50)
    condition = models.CharField(max_length=100)
    intubation = models.CharField(max_length=100)
    pregnancy = models.CharField(max_length=100)
    oxygen = models.CharField(max_length=100)
    ambulance_type = models.CharField(max_length=100)
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    payment_mode = models.CharField(max_length=100)
    duration_hours = models.IntegerField()
    duration_days = models.IntegerField()
    ambulance_number = models.CharField(max_length=20, unique=True)  # Unique ambulance number
    
    def __str__(self):
        return f"Ambulance Order for {self.patient} - Service: {self.service}"
    
    def save(self, *args, **kwargs):
        if not self.ambulance_number:
            last_ambulance = AmbulanceOrder.objects.order_by('-id').first()
            if last_ambulance:
                last_number = int(last_ambulance.ambulance_number.split('-')[-1])
            else:
                last_number = 0
            new_number = last_number + 1
            self.ambulance_number = f"AMB-{new_number:07}"  # Format the ambulance number
        super().save(*args, **kwargs)
           
class Vehicle(models.Model):
    VEHICLE_TYPES = [
        ('Ambulance', 'Ambulance'),
        ('Car', 'Car'),
        ('Van', 'Van'),
        ('Truck', 'Truck'),
        ('Motorcycle', 'Motorcycle'),
        # Add more vehicle types as needed
    ]

    vehicle_type = models.CharField(max_length=100, choices=VEHICLE_TYPES)
    activities = models.CharField(max_length=255)
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    ambulance_type = models.CharField(max_length=100)
    organization = models.CharField(max_length=255)
    contact_person = models.CharField(max_length=100)
    contact_phone = models.CharField(max_length=20)
    location = models.CharField(max_length=100)
    duration = models.IntegerField()
    days = models.IntegerField()
    payment_mode = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.vehicle_type} - {self.organization}"
               
class RemoteProcedure(models.Model):
    patient = models.ForeignKey(RemotePatient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Staffs, on_delete=models.CASCADE,blank=True, null=True)
    visit = models.ForeignKey(RemotePatientVisits, on_delete=models.CASCADE)
    consultation = models.ForeignKey(RemoteConsultationNotes, on_delete=models.CASCADE,blank=True, null=True)
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
    doctor = models.ForeignKey(Staffs, on_delete=models.CASCADE, related_name='doctor_consultations')
    created_by = models.ForeignKey(Staffs, on_delete=models.CASCADE, blank=True, null=True, related_name='created_consultations')
    patient = models.ForeignKey(Patients, on_delete=models.CASCADE)
    visit = models.ForeignKey(PatientVisits, on_delete=models.CASCADE, blank=True, null=True)
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
    appointment_number = models.CharField(max_length=20, unique=True) # Unique appointment number
    
    def __str__(self):
        return f"Appointment with {self.doctor.admin.first_name} {self.doctor.middle_name} {self.doctor.admin.last_name} for {self.patient.fullname} on {self.appointment_date} from {self.start_time} to {self.end_time}"
    
    def save(self, *args, **kwargs):       
        
        # Generate and set the appointment number if it's not already set
        if not self.appointment_number:
            last_appointment = Consultation.objects.order_by('-id').first()  # Get the last appointment
            if last_appointment:
                last_number = int(last_appointment.appointment_number.split('-')[-1])
            else:
                last_number = 0
            new_number = last_number + 1
            self.appointment_number = f"APT-{new_number:07}"  # Format the appointment number
        super().save(*args, **kwargs)  # Call the original save method
        

class ConsultationNotification(models.Model):
    consultation = models.ForeignKey(Consultation, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Staffs, on_delete=models.CASCADE)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Consultation Notification'
        verbose_name_plural = 'Consultation Notifications'

    def __str__(self):
        return f'Notification for Consultation ID: {self.consultation.id} - Doctor: {self.doctor.username}'        
class RemoteConsultation(models.Model):
    doctor = models.ForeignKey(Staffs, on_delete=models.CASCADE)
    patient = models.ForeignKey(RemotePatient, on_delete=models.CASCADE)
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
    visit = models.ForeignKey(PatientVisits, on_delete=models.CASCADE,blank=True, null=True) 
    doctor = models.ForeignKey(Staffs, on_delete=models.CASCADE,blank=True, null=True) 
    # Information about the referral
    source_location  = models.CharField(max_length=255, help_text='Source location of the patient',default="resa medical hospital")
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
  
class Counseling(models.Model):
    topic = models.CharField(max_length=100)
    description = models.TextField()
    patient = models.ForeignKey(Patients, on_delete=models.CASCADE)
    visit = models.ForeignKey(PatientVisits, on_delete=models.CASCADE,blank=True, null=True) 
    counselor = models.ForeignKey(Staffs, on_delete=models.CASCADE,blank=True, null=True) 
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.topic    
class RemoteReferral(models.Model):
    # Patient who is being referred
    patient = models.ForeignKey(RemotePatient, on_delete=models.CASCADE)   
    visit = models.ForeignKey(RemotePatientVisits, on_delete=models.CASCADE,blank=True, null=True)
    consultation = models.ForeignKey(RemoteConsultationNotes, on_delete=models.CASCADE,blank=True, null=True)
    # Information about the referral
    source_location  = models.CharField(max_length=255, help_text='Source location of the patient')
    destination_location = models.CharField(max_length=255, help_text='Destination location for MedEvac')
    rfn = models.CharField(max_length=20, unique=True, editable=False)  
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
    def save(self, *args, **kwargs):
        if not self.rfn:
            last_referral_no = RemoteReferral.objects.order_by('-id').first()
            if last_referral_no:
                last_rfn = int(last_referral_no.rfn.split('-')[-1])
                new_rfn = f"RFN-{last_rfn + 1:07d}"
            else:
                new_rfn = "RFN-0000001"
            self.rfn = new_rfn
        super().save(*args, **kwargs)

    objects = models.Manager()
    # Add more fields as needed

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
    remain_quantity = models.PositiveIntegerField(default=0)
    purchase_date = models.DateField()
    total_payment = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True) 
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
            existing_record.remain_quantity += quantity
            existing_record.save()
        else:
            # Create a new record
            cls.objects.create(
                medicine_id=medicine_id,
                quantity=quantity,
                remain_quantity=quantity, 
                purchase_date=purchase_date
            )
    
class Prescription(models.Model):
    patient = models.ForeignKey('Patients', on_delete=models.CASCADE)
    entered_by = models.ForeignKey('Staffs', on_delete=models.CASCADE,blank=True, null=True)
    medicine = models.ForeignKey('Medicine', on_delete=models.CASCADE)  # Link with Medicine model
    visit = models.ForeignKey(PatientVisits, on_delete=models.CASCADE,blank=True, null=True) # Link with Medicine model
    dose = models.CharField(max_length=50)
    frequency = models.CharField(max_length=50)
    duration = models.CharField(max_length=50)
    quantity_used = models.PositiveIntegerField()   
    total_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)    
    def __str__(self):
        return f"{self.patient.first_name} - {self.medicine.name}"  # Accessing drug's name   
    
class RemotePrescription(models.Model):
    patient = models.ForeignKey('RemotePatient', on_delete=models.CASCADE)
    medicine = models.ForeignKey('Medicine', on_delete=models.CASCADE)  # Link with Medicine model
    visit = models.ForeignKey(RemotePatientVisits, on_delete=models.CASCADE)  # Link with Medicine model
    prs_no = models.CharField(max_length=20, unique=True, editable=False)    
    dose = models.CharField(max_length=50)
    frequency = models.CharField(max_length=50)
    duration = models.CharField(max_length=50)
    quantity_used = models.PositiveIntegerField()   
    total_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def save(self, *args, **kwargs):
        # Generate a unique identifier based on count of existing records
        if not self.prs_no:
            self.prs_no = generate_remoteprescription_id()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.patient.fullname} - {self.drug.name}"  # Accessing drug's name   
    
def generate_remoteprescription_id():
    last_prescription = RemotePrescription.objects.last()
    last_sample_number = int(last_prescription.prs_no.split('-')[-1]) if last_prescription else 0
    new_prescription_id = last_sample_number + 1
    return f"PRS-{new_prescription_id:07d}"   
      
     
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
    

    
   
class HealthIssue(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    is_disease = models.BooleanField(default=True)
    
    # Additional fields
    severity = models.CharField(max_length=50, blank=True, null=True)
    treatment_plan = models.TextField(blank=True, null=True)
    onset_date = models.DateField(blank=True, null=True)
    resolution_date = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()
    # Add more fields as needed
    
    def __str__(self):
        return self.name
      
class Equipment(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)  # Description of the equipment
    manufacturer = models.CharField(max_length=100, blank=True)  # Manufacturer of the equipment
    serial_number = models.CharField(max_length=50, blank=True)  # Serial number of the equipment
    acquisition_date = models.DateField(null=True, blank=True)  # Date when the equipment was acquired
    warranty_expiry_date = models.DateField(null=True, blank=True)  # Expiry date of the warranty
    location = models.CharField(max_length=100, blank=True)  # Location where the equipment is stored
    is_active = models.BooleanField(default=True)  # Flag indicating if the equipment is currently active
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()
    
    def __str__(self):
        return self.name
    
class EquipmentMaintenance(models.Model):
    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE)
    maintenance_date = models.DateField()
    technician = models.CharField(max_length=100)  # Technician who performed the maintenance
    description = models.TextField(blank=True)  # Description of the maintenance performed
    cost = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)  # Cost of maintenance
    notes = models.TextField(blank=True)  # Additional notes or comments
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()

    def __str__(self):
        return f"{self.equipment.name} - Maintenance on {self.maintenance_date}" 
    
class Reagent(models.Model):
    name = models.CharField(max_length=100)
    expiration_date = models.DateField(blank=True, null=True)
    manufacturer = models.CharField(max_length=100)
    lot_number = models.CharField(max_length=50)
    storage_conditions = models.TextField(blank=True)
    quantity_in_stock = models.PositiveIntegerField()
    price_per_unit = models.DecimalField(max_digits=10, decimal_places=2)
    remaining_quantity = models.PositiveIntegerField()  # New field for remaining quantity
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()

    def __str__(self):
        return self.name   
    
class ReagentUsage(models.Model):
    lab_technician = models.ForeignKey(Staffs, on_delete=models.CASCADE)
    reagent = models.ForeignKey(Reagent, on_delete=models.CASCADE)
    usage_date = models.DateField()
    quantity_used = models.PositiveIntegerField()
    # Add other reagent usage-related information
    observation = models.TextField()  # Additional field for observations or notes
    technician_notes = models.TextField()  # Additional field for technician notes 
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()  
    
class QualityControl(models.Model):
    lab_technician = models.ForeignKey('Staffs', on_delete=models.CASCADE)
    control_date = models.DateField()
    # Add other quality control-related information
    control_type = models.CharField(max_length=50)  # Type of quality control performed
    result = models.CharField(max_length=50)  # Result of the quality control test
    remarks = models.TextField(blank=True)  # Additional remarks or comments

    # Add more fields as needed         
        
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
