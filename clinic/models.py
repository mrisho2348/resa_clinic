from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import BaseUserManager
from django.db.models.signals import post_save,pre_save,post_delete
from django.dispatch import receiver

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
    
# class Patient(models.Model):
    # mrn_format = models.CharField(max_length=20)  # Assuming MRN format is a string

    # # Personal Information
    # first_name = models.CharField(max_length=50)
    # middle_name = models.CharField(max_length=50)
    # last_name = models.CharField(max_length=50)
    # gender = models.CharField(max_length=10, choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')])
    # age = models.PositiveIntegerField()
    # nationality = models.CharField(max_length=50)
    # patient_type = models.CharField(max_length=20)
    # company = models.CharField(max_length=50)
    # occupation = models.CharField(max_length=50)
    # phone = models.CharField(max_length=15)
    # employee_number = models.CharField(max_length=20)
    # date_of_first_employment = models.DateField()
    # long_time_illness = models.TextField()
    # long_time_medication = models.TextField()
    # osha_certificate = models.BooleanField()
    # insurance = models.CharField(max_length=20, choices=[('Uninsured', 'Uninsured'), ('Insured', 'Insured')])

    # # Emergency Contact
    # emergency_contact_name = models.CharField(max_length=50)
    # emergency_contact_relation = models.CharField(max_length=50)
    # emergency_contact_phone = models.CharField(max_length=15)
    # emergency_contact_mobile = models.CharField(max_length=15)

    # # Health Condition
    # allergies = models.BooleanField()
    # allergies_notes = models.TextField()
    # eye_condition = models.BooleanField()
    # eye_condition_notes = models.TextField()
    # ent_conditions = models.BooleanField()
    # ent_conditions_notes = models.TextField()
    # respiratory_conditions = models.BooleanField()
    # respiratory_conditions_notes = models.TextField()
    # cardiovascular_conditions = models.BooleanField()
    # cardiovascular_conditions_notes = models.TextField()
    # urinary_conditions = models.BooleanField()
    # urinary_conditions_notes = models.TextField()
    # stomach_bowel_conditions = models.BooleanField()
    # stomach_bowel_conditions_notes = models.TextField()
    # musculoskeletal_conditions = models.BooleanField()
    # musculoskeletal_conditions_notes = models.TextField()
    # neuro_psychiatric_conditions = models.BooleanField()
    # neuro_psychiatric_conditions_notes = models.TextField()

    # # Family History
    # family_allergies = models.BooleanField()
    # family_allergies_relationship = models.CharField(max_length=50)
    # family_allergies_comments = models.TextField()
    # family_eye_condition = models.BooleanField()
    # family_eye_condition_relationship = models.CharField(max_length=50)
    # family_eye_condition_comments = models.TextField()
    # # Repeat the structure for additional family history conditions

    # # Life Style
    # smoking = models.BooleanField()
    # alcohol_consumption = models.BooleanField()
    # weekly_exercise_frequency = models.CharField(max_length=50)
    # healthy_diet = models.BooleanField()
    # stress_management = models.BooleanField()
    # sufficient_sleep = models.BooleanField()

    # def __str__(self):
    #     return f"{self.first_name} {self.last_name}"
    
    
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
