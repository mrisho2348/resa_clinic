from decimal import Decimal
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import BaseUserManager
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from clinic.models import Country, Medicine, PathodologyRecord, Staffs


    
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
    patient = models.ForeignKey('RemotePatient', on_delete=models.CASCADE, related_name='remote_medication_allergies')
    medicine_name = models.CharField(max_length=100)
    reaction = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.medicine_name} - {self.reaction}"
    
class PatientSurgery(models.Model):
    patient = models.ForeignKey('RemotePatient', on_delete=models.CASCADE)
    surgery_name = models.CharField(max_length=100,blank=True, null=True)
    surgery_date = models.TextField(blank=True, null=True)   
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()
    def __str__(self):
        return f"{self.surgery_name} - {self.surgery_date}"  
 
class HealthRecord(models.Model):    
    name = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()
    # Add more fields for health record information as needed

    def __str__(self):
        return f"{self.name}"  
    
class PatientLifestyleBehavior(models.Model):
    patient = models.ForeignKey('RemotePatient', on_delete=models.CASCADE)
    weekly_exercise_frequency =models.CharField(max_length=10, blank=True, null=True)   
    smoking = models.CharField(max_length=10, blank=True, null=True)
    alcohol_consumption = models.CharField(max_length=10, blank=True, null=True)    
    healthy_diet = models.CharField(max_length=10, blank=True, null=True)
    stress_management = models.CharField(max_length=10, blank=True, null=True)
    sufficient_sleep = models.CharField(max_length=10, blank=True, null=True)

    def __str__(self):
        return f"{self.patient}"

class MedicineRoute(models.Model):
    name = models.CharField(max_length=100)
    explanation = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()
    
    def __str__(self):
        return self.name  
    
class MedicineUnitMeasure(models.Model):
    name = models.CharField(max_length=100)
    short_name = models.CharField(max_length=20)
    application_user = models.CharField(max_length=100)  # You may want to adjust the field type as per your application requirements
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()
    
    def __str__(self):
        return self.name      

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
    nationality = models.ForeignKey(Country, on_delete=models.CASCADE) 
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
        return f"{self.first_name} {self.middle_name} {self.last_name}"   

    
class PatientHealthCondition(models.Model):
    patient = models.ForeignKey(RemotePatient, on_delete=models.CASCADE, related_name='remote_health_conditions', verbose_name='Patient')    
    health_condition = models.CharField(max_length=200, blank=True, null=True, verbose_name='Health Condition')
    health_condition_notes = models.CharField(max_length=200, blank=True, null=True, verbose_name='Health Condition Notes')  
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created At')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Updated At')
    
    objects = models.Manager()  

class FamilyMedicalHistory(models.Model):
    patient = models.ForeignKey(RemotePatient, on_delete=models.CASCADE, related_name='remote_family_medical_history', verbose_name='Patient')
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

    
class RemotePatientVital(models.Model):
    patient = models.ForeignKey('RemotePatient', on_delete=models.CASCADE)
    visit = models.ForeignKey('RemotePatientVisits', on_delete=models.CASCADE)  
    doctor = models.ForeignKey(Staffs, on_delete=models.CASCADE,blank=True, null=True)
    recorded_at = models.DateTimeField(auto_now_add=True)
    respiratory_rate = models.PositiveIntegerField(null=True, blank=True, help_text="Respiratory rate in breaths per minute")
    pulse_rate = models.PositiveIntegerField(null=True, blank=True, help_text="Pulse rate in beats per minute")
    sbp = models.CharField(max_length=20, null=True, blank=True, help_text="Systolic Blood Pressure (mmHg)")
    dbp = models.CharField(max_length=20, null=True, blank=True, help_text="Diastolic Blood Pressure (mmHg)")
    blood_pressure = models.CharField(max_length=20, null=True, blank=True, help_text="Blood pressure measurement")
    spo2 = models.PositiveIntegerField(null=True, blank=True, help_text="SPO2 measurement in percentage")
    temperature = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, help_text="Temperature measurement in Celsius",default=37.5)
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

        

class Diagnosis(models.Model):
    diagnosis_name= models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()
    
    def __str__(self):
        return self.diagnosis_name
    
    


   
class RemoteConsultationNotes(models.Model):
    doctor = models.ForeignKey(Staffs, on_delete=models.CASCADE)
    patient = models.ForeignKey(RemotePatient, on_delete=models.CASCADE)
    visit = models.ForeignKey('RemotePatientVisits', on_delete=models.CASCADE)  
    chief_complaints = models.TextField(null=True, blank=True)
    history_of_presenting_illness = models.TextField(null=True, blank=True)
    consultation_number = models.CharField(max_length=20, unique=True)
    physical_examination = models.TextField(null=True, blank=True)
    allergy_to_medications = models.CharField(max_length=255, null=True, blank=True)
    provisional_diagnosis = models.ManyToManyField(Diagnosis, related_name='remote_provisional_notes', blank=True)
    final_diagnosis = models.ManyToManyField(Diagnosis, related_name='remote_final_notes', blank=True)
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
        


class RemoteImagingRecord(models.Model):
    patient = models.ForeignKey('RemotePatient', on_delete=models.CASCADE)
    visit = models.ForeignKey('RemotePatientVisits', on_delete=models.CASCADE)
    doctor = models.ForeignKey(Staffs, on_delete=models.CASCADE,blank=True, null=True) 
    data_recorder = models.ForeignKey(Staffs, on_delete=models.CASCADE,blank=True, null=True,related_name='remote_data_recorder') 
    imaging= models.ForeignKey(RemoteService, on_delete=models.CASCADE,blank=True, null=True) 
    order_date = models.DateField(null=True, blank=True)
    description = models.TextField(blank=True, null=True)
    result = models.TextField(null=True, blank=True)   
    image = models.ImageField(upload_to='imaging_records/', null=True, blank=True)
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()

    def __str__(self):
        return f"Imaging Record for {self.patient} - {self.imaging} ({self.data_recorder})"
    
class RemoteConsultationOrder(models.Model):
    patient = models.ForeignKey('RemotePatient', on_delete=models.CASCADE)
    visit = models.ForeignKey('RemotePatientVisits', on_delete=models.CASCADE)
    doctor = models.ForeignKey(Staffs, on_delete=models.CASCADE,blank=True, null=True) 
    data_recorder = models.ForeignKey(Staffs, on_delete=models.CASCADE,blank=True, null=True,related_name='remote_consultation_data_recorder') 
    consultation= models.ForeignKey(RemoteService, on_delete=models.CASCADE,blank=True, null=True) 
    order_date = models.DateField(null=True, blank=True)
    description = models.TextField(blank=True, null=True)   
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()
    def __str__(self):
        return f"Consultation Order for {self.patient} - {self.data_recorder} ({self.order_date})"


        
class RemoteLaboratoryOrder(models.Model):
    patient = models.ForeignKey(RemotePatient, on_delete=models.CASCADE)
    visit = models.ForeignKey(RemotePatientVisits, on_delete=models.CASCADE,blank=True, null=True) 
    doctor = models.ForeignKey(Staffs, on_delete=models.CASCADE,blank=True, null=True) 
    data_recorder = models.ForeignKey(Staffs, on_delete=models.CASCADE,blank=True, null=True,related_name='remote_lab_data_recorder') 
    name = models.ForeignKey(RemoteService, on_delete=models.CASCADE,blank=True, null=True) 
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
            last_lab_number = RemoteLaboratoryOrder.objects.order_by('-id').first()  # Get the last appointment
            if last_lab_number:
                last_number = int(last_lab_number.lab_number.split('-')[-1])
            else:
                last_number = 0
            new_number = last_number + 1
            self.lab_number = f"LAB-{new_number:07}"  # Format the appointment number
        super().save(*args, **kwargs)  # Call the original save method
   

class RemoteHospitalVehicle(models.Model):
    number = models.CharField(max_length=50)
    plate_number = models.CharField(max_length=50)
    is_active = models.BooleanField(default=True)
    vehicle_type = models.CharField(max_length=100)  # New field for vehicle type
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()

    def __str__(self):
        return self.number   
    
class RemoteAmbulanceRoute(models.Model):
    from_location = models.CharField(max_length=100)
    to_location = models.CharField(max_length=100)
    distance = models.FloatField()
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    profit = models.DecimalField(max_digits=10, decimal_places=2)
    advanced_ambulance_cost = models.DecimalField(max_digits=10, decimal_places=2)
    total = models.FloatField(editable=False)  # Make total field read-only
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()

    def save(self, *args, **kwargs):
        # Convert cost and profit to Decimal objects
        cost = Decimal(str(self.cost))
        profit = Decimal(str(self.profit))

        # Calculate total using Decimal arithmetic
        self.total = cost + profit

        super(RemoteAmbulanceRoute, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.from_location} to {self.to_location}"       
    
    
class RemoteAmbulanceActivity(models.Model):
    name = models.CharField(max_length=100)
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    profit = models.DecimalField(max_digits=10, decimal_places=2)
    total = models.DecimalField(max_digits=10, decimal_places=2, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()
    
    def save(self, *args, **kwargs):
        # Convert cost and profit to Decimal objects
        cost = Decimal(str(self.cost))
        profit = Decimal(str(self.profit))

        # Calculate total using Decimal arithmetic
        self.total = cost + profit

        super(RemoteAmbulanceActivity, self).save(*args, **kwargs)

    def __str__(self):
        return self.name    
        
class RemoteAmbulanceOrder(models.Model):
    patient = models.ForeignKey(RemotePatient, on_delete=models.CASCADE)
    visit = models.ForeignKey(RemotePatientVisits, on_delete=models.CASCADE, blank=True, null=True) 
    data_recorder = models.ForeignKey(Staffs, on_delete=models.CASCADE,blank=True, null=True,related_name='remote_ambulance_data_recorder') 
    service = models.CharField(max_length=100)
    from_location = models.CharField(max_length=100)
    to_location = models.CharField(max_length=100)
    order_date = models.DateField(null=True, blank=True)  
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
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    ambulance_number = models.CharField(max_length=20, unique=True)  # Unique ambulance number
    objects = models.Manager()
    
    def __str__(self):
        return f"Ambulance Order for {self.patient} - Service: {self.service}"
    
    def save(self, *args, **kwargs):
        if not self.ambulance_number:
            last_ambulance = RemoteAmbulanceOrder.objects.order_by('-id').first()
            if last_ambulance:
                last_number = int(last_ambulance.ambulance_number.split('-')[-1])
            else:
                last_number = 0
            new_number = last_number + 1
            self.ambulance_number = f"AMB-{new_number:07}"  # Format the ambulance number
        super().save(*args, **kwargs)
           
class RemoteAmbulanceVehicleOrder(models.Model):
    vehicle_type = models.CharField(max_length=100,blank=True, null=True)
    activities = models.CharField(max_length=255,blank=True, null=True)
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    ambulance_number = models.CharField(max_length=100,blank=True, null=True)
    organization = models.CharField(max_length=255,blank=True, null=True)
    contact_person = models.CharField(max_length=100,blank=True, null=True)
    contact_phone = models.CharField(max_length=20,blank=True, null=True)
    location = models.CharField(max_length=100,blank=True, null=True)
    duration = models.IntegerField()
    days = models.IntegerField()
    payment_mode = models.CharField(max_length=100,blank=True, null=True)
    order_date = models.DateField(null=True, blank=True) 
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True) 
    objects = models.Manager()

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
    

class RemoteOrder(models.Model):

    ORDER_STATUS = [
        ('Paid', 'Paid'),
        ('Unpaid', 'Unpaid'),
    ]

    ORDER_NUMBER_PREFIX = 'ORD'  # Prefix for the order number

    order_date = models.DateField(default=timezone.now, null=True, blank=True)
    order_type =  models.TextField(blank=True, null=True)
    patient = models.ForeignKey('RemotePatient', on_delete=models.CASCADE)
    visit = models.ForeignKey(RemotePatientVisits, on_delete=models.CASCADE,blank=True, null=True)
    added_by = models.ForeignKey(Staffs, on_delete=models.CASCADE,blank=True, null=True)
    doctor = models.ForeignKey(Staffs, on_delete=models.CASCADE,blank=True, null=True,related_name='remote_doctor')
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    is_read = models.BooleanField(default=False)
    status = models.CharField(max_length=100, choices=ORDER_STATUS, default='Unpaid')
    order_number = models.CharField(max_length=12, unique=True)

    def __str__(self):
        return f"{self.order_type} Order for {self.patient}"

    def save(self, *args, **kwargs):
        if not self.order_number:
            last_order = RemoteOrder.objects.order_by('-id').first()
            if last_order:
                last_number = int(last_order.order_number.split('-')[-1])  # Extract the numeric part
            else:
                last_number = 0
            new_number = last_number + 1
            self.order_number = f"{self.ORDER_NUMBER_PREFIX}-{new_number:07}"  # Format the order number
        super().save(*args, **kwargs)
    

     
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


class RemoteCounseling(models.Model):
    topic = models.CharField(max_length=100)
    description = models.TextField()
    patient = models.ForeignKey(RemotePatient, on_delete=models.CASCADE)
    visit = models.ForeignKey(RemotePatientVisits, on_delete=models.CASCADE,blank=True, null=True) 
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
   



class ChiefComplaint(models.Model):    
    patient = models.ForeignKey(RemotePatient, on_delete=models.CASCADE)
    visit = models.ForeignKey(RemotePatientVisits, on_delete=models.CASCADE,blank=True, null=True)
    health_record = models.ForeignKey(HealthRecord, on_delete=models.CASCADE,blank=True, null=True)
    other_complaint = models.CharField(max_length=100)
    duration = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()
    # Other fields for Chief Complaint
    def __str__(self):
        return f"{self.health_record.name} - {self.duration}"    
    
class PrimaryPhysicalExamination(models.Model):
    patient = models.ForeignKey(RemotePatient, on_delete=models.CASCADE)
    visit = models.ForeignKey(RemotePatientVisits, on_delete=models.CASCADE,blank=True, null=True)
    airway = models.CharField(max_length=200,blank=True, null=True)
    patent_airway = models.CharField(max_length=200,blank=True, null=True)
    notpatient_explanation = models.TextField(blank=True, null=True)
    breathing = models.CharField(max_length=200,blank=True, null=True)
    normal_breathing = models.TextField(blank=True, null=True)
    abnormal_breathing = models.CharField(max_length=200,blank=True, null=True)
    circulating = models.CharField(max_length=200,blank=True, null=True)
    normal_circulating = models.TextField(blank=True, null=True)
    abnormal_circulating = models.CharField(max_length=200,blank=True, null=True)    
    gcs = models.CharField(max_length=200,blank=True, null=True)
    rbg = models.CharField(max_length=200,blank=True, null=True)
    pupil = models.CharField(max_length=200,blank=True, null=True)
    pain_score = models.CharField(max_length=200,blank=True, null=True)
    avpu = models.CharField(max_length=200,blank=True, null=True)
    exposure = models.CharField(max_length=200,blank=True, null=True)
    normal_exposure = models.CharField(max_length=200,blank=True, null=True)
    abnormal_exposure = models.CharField(max_length=200,blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()

    def __str__(self):
        return f"Physical Examination - {self.pk}"
    
class SecondaryPhysicalExamination(models.Model):
    patient = models.ForeignKey(RemotePatient, on_delete=models.CASCADE)
    visit = models.ForeignKey(RemotePatientVisits, on_delete=models.CASCADE,blank=True, null=True)
    heent = models.CharField(max_length=50, blank=True, null=True)
    cns = models.CharField(max_length=50, blank=True, null=True)
    normal_cns = models.CharField(max_length=50, blank=True, null=True)
    abnormal_cns = models.CharField(max_length=50, blank=True, null=True)
    cvs = models.CharField(max_length=50, blank=True, null=True)
    normal_cvs = models.CharField(max_length=50, blank=True, null=True)
    abnormal_cvs = models.CharField(max_length=50, blank=True, null=True)
    rs = models.CharField(max_length=50, blank=True, null=True)
    normal_rs = models.CharField(max_length=50, blank=True, null=True)
    abnormal_rs = models.CharField(max_length=50, blank=True, null=True)
    pa = models.CharField(max_length=50, blank=True, null=True)
    normal_pa = models.CharField(max_length=50, blank=True, null=True)
    abnormal_pa = models.CharField(max_length=50, blank=True, null=True)
    gu = models.CharField(max_length=100, blank=True, null=True)
    normal_gu = models.CharField(max_length=100, blank=True, null=True)
    abnormal_gu = models.CharField(max_length=100, blank=True, null=True)
    mss = models.CharField(max_length=100, blank=True, null=True)    
    normal_mss = models.CharField(max_length=100, blank=True, null=True)    
    abnormal_mss = models.CharField(max_length=100, blank=True, null=True)    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()
    
    def __str__(self):
        return self.pk

  
    
    
class RemotePrescription(models.Model):
    VERIFICATION_CHOICES = (
        ('verified', 'Verified'),
        ('not_verified', 'Not Verified'),
    )

    ISSUE_CHOICES = (
        ('issued', 'Issued'),
        ('not_issued', 'Not Issued'),
    )

    patient = models.ForeignKey('RemotePatient', on_delete=models.CASCADE)
    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE)  # Link with Medicine model
    visit = models.ForeignKey(RemotePatientVisits, on_delete=models.CASCADE)  # Link with Medicine model
    prs_no = models.CharField(max_length=20, unique=True, editable=False)    
    dose = models.CharField(max_length=50)
    frequency = models.CharField(max_length=50)
    duration = models.CharField(max_length=50)
    quantity_used = models.PositiveIntegerField()   
    verified = models.CharField(max_length=20, choices=VERIFICATION_CHOICES, default='not_verified')
    issued = models.CharField(max_length=20, choices=ISSUE_CHOICES, default='not_issued')
    status = models.CharField(max_length=20, choices=[('paid', 'Paid'), ('unpaid', 'Unpaid')], default='unpaid')

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




      

    
    
        

