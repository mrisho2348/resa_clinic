from datetime import date, datetime
import json
from django.utils import timezone
import logging
from django.db import models
from django.db import IntegrityError
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth import logout,login
from django.http import Http404, HttpResponse, HttpResponseBadRequest,HttpResponseRedirect
from django.template import loader
from django.shortcuts import render
from django.urls import reverse
from django.db.models import F
from django.views.decorators.csrf import csrf_protect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.views.generic.edit import FormView
from django.contrib.messages.views import SuccessMessageMixin
from django.core.mail import send_mail
from clinic.emailBackEnd import EmailBackend
from django.core.exceptions import ObjectDoesNotExist
from clinic.forms import ImportStaffForm
from clinic.models import Company, Consultation, ContactDetails, CustomUser, DiseaseRecode, InsuranceCompany, Medicine, MedicineInventory, Notification, NotificationMedicine, PathodologyRecord, Patients, Procedure, Staffs
from clinic.resources import StaffResources
from tablib import Dataset
from django.views.decorators.http import require_POST
from django.contrib.contenttypes.models import ContentType
from django.db.models import OuterRef, Subquery
from .models import Category, ConsultationFee, ConsultationNotes, Diagnosis, DiagnosticTest, Diagnosis, Equipment, EquipmentMaintenance, FamilyMedicalHistory, HealthIssue, InventoryItem, MedicationPayment, PathologyDiagnosticTest, PatientDisease, PatientHealthCondition, PatientVisits, PatientVital, Prescription, Procedure, Patients, QualityControl, Reagent, ReagentUsage, Referral, RemotePatient, RemotePatientVisits, RemotePrescription, Sample, Service, Supplier, UsageHistory

# Create your views here.
def index(request):
    return render(request,"index.html")

def dashboard(request):
    total_patients = Patients.objects.count()
    recently_added_patients = Patients.objects.order_by('-created_at')[:6]
    doctors = Staffs.objects.filter(role='doctor')
    context = {
        'total_patients': total_patients,
        'recently_added_patients': recently_added_patients,
        'doctors': doctors,
        # 'gender_based_monthly_counts': gender_based_monthly_counts,
    }
    return render(request,"hod_template/home_content.html",context)

def contact(request):
    return render(request,"contact.html")
def blog_single(request):
    return render(request,"blog-single.html")
def page_404(request):
    return render(request,"404.html")


def ShowLogin(request):  
  return render(request,'login.html')



def DoLogin(request):
    if request.method != "POST":
        return HttpResponse("<h2>Method Not allowed</h2>")
    else:
        user = EmailBackend.authenticate(request, request.POST.get("email"), request.POST.get("password"))
        if user is not None:
            if not user.is_active:
                messages.error(request, "Your account is not active. Please contact the administrator for support.")
                return HttpResponseRedirect(reverse("login"))

            login(request, user)
            if user.user_type == "1":
                return HttpResponseRedirect(reverse("dashboard"))
            elif user.user_type == "2":
                return HttpResponseRedirect(reverse("dashboard"))             
            else:
                return HttpResponseRedirect(reverse("login"))
        else:
            messages.error(request, "Invalid Login Details")
            return HttpResponseRedirect(reverse("login"))
    
    
def GetUserDetails(request):
  user = request.user
  if user.is_authenticated:
    return HttpResponse("User : "+user.email+" usertype : " + user.usertype)
  else:
    return HttpResponse("Please login first")   
  
  
def logout_user(request):
  logout(request)
  return HttpResponseRedirect(reverse("home"))
    
class ContactFormView(SuccessMessageMixin, FormView):
    template_name = 'contact_form.html'
    form_class = None  # No Django form is used
    success_url = '/success/'  # Set the URL where users should be redirected on success
    success_message = "Your message was submitted successfully. We'll get back to you soon."

    def form_valid(self, form):
        try:
            # Process the form data
            your_name = self.request.POST.get('your_name')
            your_email = self.request.POST.get('your_email')
            your_subject = self.request.POST.get('your_subject', '')
            your_message = self.request.POST.get('your_message')

            # Save to the model (optional)
            ContactDetails.objects.create(
                your_name=your_name,
                your_email=your_email,
                your_subject=your_subject,
                your_message=your_message
            )

            # Send email to the administrator
            send_mail(
                f'New Contact Form Submission: {your_subject}',
                f'Name: {your_name}\nEmail: {your_email}\nMessage: {your_message}',
                'from@example.com',  # Sender's email address
                ['mrishohamisi2348@gmail.com'],  # Administrator's email address
                fail_silently=False,
            )

            messages.success(self.request, self.get_success_message())
            return self.form_valid_redirection(self.form_valid_redirect())
        except Exception as e:
            messages.error(self.request, f"An error occurred: {str(e)}")
            return self.form_invalid(self.get_form())

    def form_invalid(self, form):
        # Handle the case where the form is invalid
        return self.render_to_response(self.get_context_data(form=form))

    def form_valid_redirection(self, redirect_to):
        return self.render_to_response({'redirect_to': redirect_to})

    def form_valid_redirect(self):
        return self.get_success_url()    


def portfolio_details(request):
    return render(request,"portfolio-details.html")

@login_required
def manage_patient(request):
    patient_records=Patients.objects.all() 
    return render(request,"hod_template/manage_patients.html", {"patient_records":patient_records})
# @login_required
# def remotemanage_patient(request):
#     patient_records=Patients.objects.all() 
#     return render(request,"hod_template/remote_manage_patients.html", {"patient_records":patient_records})

@login_required
def manage_consultation(request):
    patients=Patients.objects.all() 
    pathology_records=PathodologyRecord.objects.all() 
    doctors=Staffs.objects.filter(role='doctor')
    context = {
        'patients':patients,
        'pathology_records':pathology_records,
        'doctors':doctors,
    }
    return render(request,"hod_template/manage_consultation.html",context)

@login_required
def add_consultation(request):
    return render(request,"hod_template/add_consultation.html")

@login_required
def add_request(request):
    return render(request,"hod_template/add_request.html")

@login_required
def manage_company(request):
    companies=Company.objects.all() 
    return render(request,"hod_template/manage_company.html",{"companies":companies})

@login_required
def manage_disease(request):
    disease_records=DiseaseRecode.objects.all() 
    return render(request,"hod_template/manage_disease.html",{"disease_records":disease_records})

@login_required
def manage_staff(request):     
    staffs=Staffs.objects.all()  
    return render(request,"hod_template/manage_staff.html",{"staffs":staffs})  

@login_required
def manage_insurance(request):
    insurance_companies=InsuranceCompany.objects.all() 
    return render(request,"hod_template/manage_insurance.html",{"insurance_companies":insurance_companies})

@login_required
def resa_report(request):
    return render(request,"hod_template/resa_reports.html")

@login_required
def manage_service(request):
    services=Service.objects.all()
    context = {
        'services':services
    }
    return render(request,"hod_template/manage_service.html",context)

def manage_adjustment(request):
    return render(request,"hod_template/manage_adjustment.html")

@login_required
def reports_adjustments(request):
    return render(request,"hod_template/reports_adjustments.html")

@login_required
def reports_by_visit(request):
    return render(request,"hod_template/reports_by_visit.html")

@login_required
def reports_comprehensive(request):
    return render(request,"hod_template/reports_comprehensive.html")

@login_required
def reports_patients_visit_summary(request):
    return render(request,"hod_template/reports_patients_visit_summary.html")

@login_required
def reports_patients(request):
    return render(request,"hod_template/reports_patients.html")

@login_required
def reports_service(request):
    return render(request,"hod_template/reports_service.html")

@login_required
def reports_stock_ledger(request):
    return render(request,"hod_template/reports_stock_ledger.html")

def reports_stock_level(request):
    return render(request,"hod_template/reports_stock_level.html")

@login_required
def reports_orders(request):
    return render(request,"hod_template/reports_orders.html")

@login_required
def individual_visit(request):
    return render(request,"hod_template/reports_individual_visit.html")

@login_required
def product_summary(request):
    return render(request,"hod_template/product_summary.html")

@login_required
def manage_pathodology(request):
    pathodology_records=PathodologyRecord.objects.all() 
    disease_records=DiseaseRecode.objects.all() 
    return render(request,"hod_template/manage_pathodology.html",{
        "pathodology_records":pathodology_records,
        "disease_records":disease_records,
        })


logger = logging.getLogger(__name__)

@csrf_exempt
@login_required
def save_staff_view(request):
    if request.method == 'POST':
        try:
            # Retrieve form data from the POST request
            first_name = request.POST.get('firstName')
            middle_name = request.POST.get('middleName')
            lastname = request.POST.get('lastname')            
            gender = request.POST.get('gender')
            dob = request.POST.get('dob')
            phone = request.POST.get('phone')
            profession = request.POST.get('profession')            
            marital_status = request.POST.get('maritalStatus')
            email = request.POST.get('email')
            password = request.POST.get('password')            
            user_role = request.POST.get('userRole')

            # Create a new CustomUser instance (if not exists) and link it to Staffs
            user = CustomUser.objects.create_user(username=email, password=password, email=email, first_name=first_name, last_name=lastname, user_type=2)

            # Create a new Staffs instance and link it to the user
            
            user.staff.middle_name = middle_name
            user.staff.date_of_birth = dob
            user.staff.gender = gender            
            user.staff.phone_number = phone            
            user.staff.marital_status = marital_status
            user.staff.profession = profession
            user.staff.role = user_role
        
            # Save the staff record
            user.save()

            # For demonstration purposes, you can log the saved data
            logger.info(f'Data saved successfully: {user.staff.__dict__}')

            # Return a success response to the user
            return JsonResponse({'message': 'Data saved successfully'}, status=200)
        except Exception as e:
            # Handle exceptions and log the error
            logger.error(f'Error saving data: {str(e)}')
            return JsonResponse({'error': str(e)}, status=400)

    # Return an error response if the request is not POST
    return JsonResponse({'error': 'Invalid request method'}, status=405)
    
def update_staff_status(request):
    try:
        if request.method == 'POST':
            # Get the user_id and is_active values from POST data
            user_id = request.POST.get('user_id')
            is_active = request.POST.get('is_active')

            # Retrieve the staff object or return a 404 response if not found
            staff = get_object_or_404(CustomUser, id=user_id)

            # Toggle the is_active status based on the received value
            if is_active == '1':
                staff.is_active = False
            elif is_active == '0':
                staff.is_active = True
            else:
                messages.error(request, 'Invalid request')
                return redirect('manage_staff')  # Make sure 'manage_staffs' is the name of your staff list URL

            staff.save()
            messages.success(request, 'Status updated successfully')
        else:
            messages.error(request, 'Invalid request method')
    except Exception as e:
        messages.error(request, f'An error occurred: {str(e)}')

    # Redirect back to the staff list page
    return redirect('manage_staff')  # Make sure 'manage_staffs' is the name of your staff list URL

def update_equipment_status(request):
    try:
        if request.method == 'POST':
            # Get the user_id and is_active values from POST data
            equipment_id = request.POST.get('equipment_id')
            is_active = request.POST.get('is_active')

            # Retrieve the staff object or return a 404 response if not found
            equipment = get_object_or_404(Equipment, id=equipment_id)

            # Toggle the is_active status based on the received value
            if is_active == '1':
                equipment.is_active = False
            elif is_active == '0':
                equipment.is_active = True
            else:
                messages.error(request, 'Invalid request')
                return redirect('equipment_list')  # Make sure 'manage_staffs' is the name of your staff list URL

            equipment.save()
            messages.success(request, 'equipment updated successfully')
        else:
            messages.error(request, 'Invalid request method')
    except Exception as e:
        messages.error(request, f'An error occurred: {str(e)}')

    # Redirect back to the staff list page
    return redirect('equipment_list')  # Make sure 'manage_staffs' is the name of your staff list URL

def edit_staff(request, staff_id):
    # Check if the staff with the given ID exists, or return a 404 page
    staff = get_object_or_404(Staffs, id=staff_id)  
    # If staff exists, proceed with the rest of the view
    request.session['staff_id'] = staff_id
    return render(request, "update/edit_staff.html", {"id": staff_id, "username": staff.admin.username, "staff": staff})   


def edit_staff_save(request):
    if request.method == "POST":
        try:
            # Retrieve the staff ID from the session
            staff_id = request.session.get('staff_id')
            if staff_id is None:
                messages.error(request, "Staff ID not found")
                return redirect("manage_staff")

            # Retrieve the staff instance from the database
            try:
                staff = Staffs.objects.get(id=staff_id)
            except ObjectDoesNotExist:
                messages.error(request, "Staff not found")
                return redirect("manage_staff")

            # Extract the form data
            first_name = request.POST.get('firstName')
            middle_name = request.POST.get('middleName')
            lastname = request.POST.get('lastname')            
            gender = request.POST.get('gender')
            dob = request.POST.get('date_of_birth')
            phone = request.POST.get('phone')
            profession = request.POST.get('profession')            
            marital_status = request.POST.get('maritalStatus')
            email = request.POST.get('email')                        
            user_role = request.POST.get('userRole')    
          

            # Save the staff details
   
            staff.admin.first_name = first_name
            staff.admin.last_name = lastname
            staff.admin.email = email
            staff.middle_name = middle_name
            staff.role = user_role
            staff.profession = profession
            staff.marital_status = marital_status
            staff.date_of_birth = dob
            staff.phone_number = phone
            staff.gender = gender      
            staff.save()

            # Assuming the URL name for the next editing form is "qualification_form"
            messages.success(request, "Staff details updated successfully.")
            return redirect("manage_staff")
        except Exception as e:
            messages.error(request, f"Error updating staff details: {str(e)}")

    return redirect("edit_staff",staff_id=staff_id)




def single_staff_detail(request, staff_id):
    staff = get_object_or_404(Staffs, id=staff_id)
    # Fetch additional staff-related data  
    context = {
        'staff': staff,
     
    }

    return render(request, "hod_template/staff_details.html", context)

def view_patient(request, patient_id):
    patient = get_object_or_404(Patients, id=patient_id)
    # Fetch additional staff-related data  
    context = {
        'patient': patient,
     
    }

    return render(request, "hod_template/patients_detail.html", context)

def appointment_view(request, patient_id):
    try:
        if request.method == 'POST':
            # Extract data from the request
            doctor_id = request.POST.get('doctor')
            date_of_consultation = request.POST.get('date_of_consultation')
            start_time = request.POST.get('start_time')
            end_time = request.POST.get('end_time')
            description = request.POST.get('description')

            # Create a Consultation instance
            doctor = get_object_or_404(Staffs, id=doctor_id)
            patient = get_object_or_404(Patients, id=patient_id)
            consultation = Consultation(
                doctor=doctor,
                patient=patient,
                appointment_date=date_of_consultation,
                start_time=start_time,
                end_time=end_time,
                description=description
            )
            consultation.save()

            # Create a notification for the patient
            notification_message = f"New appointment scheduled with Dr. { doctor.admin.first_name } { doctor.middle_name } { doctor.admin.last_name } on {date_of_consultation} from {start_time} to {end_time}."
            Notification.objects.create(
                content_type=ContentType.objects.get_for_model(Patients),
                object_id=patient.id,
                message=notification_message
            )

            messages.success(request, "Appointment created successfully.")
            return redirect('appointment_view', patient_id=patient_id)

        # If the request is not a POST, handle the GET request
        patient = get_object_or_404(Patients, id=patient_id)
        doctors = Staffs.objects.filter(role='doctor')

        context = {
            'patient': patient,
            'doctors': doctors,
        }

        return render(request, "hod_template/add_consultation.html", context)

    except IntegrityError as e:
        # Handle integrity error (e.g., duplicate entry)
        messages.error(request, f"Error creating appointment: {str(e)}")
        return redirect('appointment_view', patient_id=patient_id)
    except Exception as e:
        # Handle other exceptions
        messages.error(request, f"An unexpected error occurred: {str(e)}")
        return JsonResponse({'status': 'error', 'message': str(e)})
    
@csrf_exempt
def appointment_view_remote(request, patient_id):
    try:
        if request.method == 'POST':
            # Extract data from the request
            doctor_id = request.POST.get('doctor')
            date_of_consultation = request.POST.get('date_of_consultation')
            start_time = request.POST.get('start_time')
            end_time = request.POST.get('end_time')
            description = request.POST.get('description')

            # Check if all required fields are present
            if not (doctor_id and date_of_consultation and start_time and end_time):
                return JsonResponse({'status': 'error', 'message': 'Missing required fields'})

            # Retrieve doctor and patient instances
            doctor = get_object_or_404(Staffs, id=doctor_id)
            patient = get_object_or_404(Patients, id=patient_id)

            # Create a Consultation instance
            consultation = Consultation(
                doctor=doctor,
                patient=patient,
                appointment_date=date_of_consultation,
                start_time=start_time,
                end_time=end_time,
                description=description
            )
            consultation.save()

            # Create a notification for the patient
            notification_message = f"New appointment scheduled with Dr. { doctor.admin.get_full_name() } on {date_of_consultation} from {start_time} to {end_time}."
            Notification.objects.create(
                content_type=ContentType.objects.get_for_model(Patients),
                object_id=patient.id,
                message=notification_message
            )

            messages.success(request, "Appointment created successfully.")
            return JsonResponse({'status': 'success'})
       
    except IntegrityError as e:
        # Handle integrity error (e.g., duplicate entry)
        messages.error(request, f"Error creating appointment: {str(e)}")
        return JsonResponse({'status': 'error', 'message': str(e)})
    except Exception as e:
        # Handle other exceptions
        messages.error(request, f"An unexpected error occurred: {str(e)}")
        return JsonResponse({'status': 'error', 'message': 'An unexpected error occurred'})

    # Handle invalid request method
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})

    
def notification_view(request):
    notifications = Notification.objects.filter(is_read=False)
    
    # Mark notifications as read when the user accesses them
    for notification in notifications:
        notification.is_read = True
        notification.save()
    
    context = {'notifications': notifications}
    return render(request, 'hod_template/manage_notification.html', context)

def confirm_meeting(request, appointment_id):
    try:
        # Retrieve the appointment
        appointment = get_object_or_404(Consultation, id=appointment_id)

        if request.method == 'POST':
            # Get the selected status from the form
            selected_status = int(request.POST.get('status'))

            # Check if the appointment is not already confirmed
            if not appointment.status:
                # Perform the confirmation action (e.g., set status to selected status)
                appointment.status = selected_status
                appointment.save()

                # Add a success message
                messages.success(request, f"Meeting with {appointment.patient.fullname} confirmed.")
            else:
                messages.warning(request, f"Meeting with {appointment.patient.fullname} is already confirmed.")
        else:
            messages.warning(request, "Invalid request method for confirming meeting.")

    except IntegrityError as e:
        # Handle IntegrityError (e.g., database constraint violation)
        messages.error(request, f"Error confirming meeting: {str(e)}")

    return redirect('appointment_list')  # Adjust the URL name based on your actual URL structure

def edit_meeting(request, appointment_id):
    try:
        if request.method == 'POST':
            start_time = request.POST.get('start_time')
            end_time = request.POST.get('end_time')

            appointment = get_object_or_404(Consultation, id=appointment_id)

            # Perform the edit action (e.g., update start time and end time)
            appointment.start_time = start_time
            appointment.end_time = end_time
            appointment.save()

            messages.success(request, f"Meeting time for {appointment.patient.fullname} edited successfully.")
    except Exception as e:
        messages.error(request, f"Error editing meeting time: {str(e)}")

    return redirect('appointment_list')

@login_required
def medicine_list(request):
    # Retrieve medicines and check for expired ones
    medicines = Medicine.objects.all()
    expired_medicines = medicines.filter(expiration_date__lt=timezone.now())

    # Create notifications for expired medicines
    for medicine in expired_medicines:
        message = f"The medicine '{medicine.name}' has expired."
        NotificationMedicine.objects.create(user=request.user, message=message)

    # Get unread notifications
    unread_notifications = NotificationMedicine.objects.filter(user=request.user, is_read=False)

    # Render the template with medicine data and notifications
    return render(request, 'hod_template/manage_medicine.html', {'medicines': medicines, 'unread_notifications': unread_notifications})

@csrf_exempt
@login_required
def add_medicine(request):
    if request.method == 'POST':
        try:
            # Retrieve data from the form
            name = request.POST['name']
            medicine_type = request.POST['medicine_type']
            side_effect = request.POST.get('side_effect', '')
            dosage = request.POST['dosage']
            storage_condition = request.POST['storage_condition']
            manufacturer = request.POST['manufacturer']
            description = request.POST.get('description', '')
            expiration_date = request.POST['expiration_date']
            unit_price = request.POST['unit_price']

            # Validate expiration date
            if expiration_date <= str(date.today()):                
                return JsonResponse({'error': 'The expiration date cannot be in the past'}, status=500)

            # Save the data to the Medicine model
            medicine = Medicine.objects.create(
                name=name,
                medicine_type=medicine_type,
                side_effect=side_effect,
                dosage=dosage,
                storage_condition=storage_condition,
                manufacturer=manufacturer,
                description=description,
                expiration_date=expiration_date,
                unit_price=unit_price
            )

           
            return JsonResponse({'message': 'Medicine added successfully'}, status=200)

        except Exception as e:            
            logger.error(f"Error adding Medicine: {str(e)}")
            return JsonResponse({'error': 'Failed to add Medicine'}, status=500)

    return JsonResponse({'error': 'Failed to add Medicine'}, status=500)

@require_POST
def add_inventory(request):
    if request.method == 'POST':
        try:
            # Retrieve data from the POST request
            medicine_id = request.POST.get('medicine_id')
            quantity = request.POST.get('quantity')
            purchase_date = request.POST.get('purchase_date')

            # Perform basic validation
            if not medicine_id or not quantity or not purchase_date:
                # Handle validation error, redirect or display an error message
                return redirect('error_page')  # Adjust the URL as needed

            # Convert the quantity to an integer
            quantity = int(quantity)

            # Convert the purchase date to a datetime object
            purchase_date = datetime.strptime(purchase_date, '%Y-%m-%d').date()

            # Call the helper method to update or create the inventory
            MedicineInventory.update_or_create_inventory(medicine_id, quantity, purchase_date)

            # Perform additional processing if needed

            # Redirect to a success page or the medicine details page
            return redirect('medicine_inventory')  # Adjust the URL as needed

        except (ValueError, TypeError):
            # Handle invalid data types, redirect or display an error message
            return redirect('medicine_list')  # Adjust the URL as needed

    else:
        # Handle non-POST requests, redirect or display an error message
        return redirect('medicine_list')  # Adjust the URL as needed
    
def medicine_inventory_list(request):
    # Retrieve all medicine inventories
    medicine_inventories = MedicineInventory.objects.all()

    # Retrieve medicines with quantity below 100
    low_quantity_medicines = MedicineInventory.objects.filter(quantity__lt=100)
    current_date = timezone.now().date()
    non_expired_medicines = Medicine.objects.filter(expiration_date__gte=current_date)
    total_payment = sum(inventory.total_payment for inventory in medicine_inventories)

    # Pass the context variables to the template
    context = {
        'medicine_inventories': medicine_inventories,
        'low_quantity_medicines': low_quantity_medicines,
        'non_expired_medicines': non_expired_medicines,
        'total_payment': total_payment,
    }

    return render(request, 'hod_template/manage_medical_inventory.html', context)

def medicine_expired_list(request):
    # Get all medicines
    all_medicines = Medicine.objects.all()

    # Filter medicines with less than or equal to 10 days remaining for expiration
    medicines = []
    for medicine in all_medicines:
        days_remaining = (medicine.expiration_date - timezone.now().date()).days
        if days_remaining <= 10:
            medicines.append({
                'name': medicine.name,
                'expiration_date': medicine.expiration_date,
                'days_remaining': days_remaining,
            })

    return render(request, 'hod_template/manage_medicine_expired.html', {'medicines': medicines})

def patient_procedure_view(request):
    template_name = 'hod_template/manage_procedure.html'
    
    # Query to retrieve the latest procedure record for each patient
    procedures = Procedure.objects.filter(
        patient=OuterRef('id')
    ).order_by('-created_at')[:1]

    # Query to retrieve patients with their corresponding procedure (excluding patients without procedures)
    patients_with_procedures = Patients.objects.annotate(
        procedure_name=Subquery(procedures.values('name')[:1]),
        procedure_description=Subquery(procedures.values('description')[:1]),
        procedure_duration=Subquery(procedures.values('duration_time')[:1]),
        procedure_equipments=Subquery(procedures.values('equipments_used')[:1]),
        procedure_cost=Subquery(procedures.values('cost')[:1])
    ).filter(procedure_name__isnull=False)
    
    patients = Patients.objects.all()
    # Retrieve the data
    data = patients_with_procedures.values(
        'id', 'mrn', 'procedure_name', 'procedure_description',
        'procedure_duration', 'procedure_equipments', 'procedure_cost'
    )

    return render(request, template_name, {'data': data,'patients':patients})



def patient_procedure_history_view(request, mrn):
    patient = get_object_or_404(Patients, mrn=mrn)
    
    # Retrieve all procedures for the specific patient
    procedures = Procedure.objects.filter(patient=patient)
    
    context = {
        'patient': patient,
        'procedures': procedures,
    }

    return render(request, 'hod_template/manage_patient_procedure.html', context)


@csrf_exempt  # Use csrf_exempt decorator for simplicity in this example. For a production scenario, consider using csrf protection.
def save_procedure(request):
    if request.method == 'POST':
        try:
            mrn = request.POST.get('mrn')
            name = request.POST.get('name')
            start_time_str = request.POST.get('start_time')
            end_time_str = request.POST.get('end_time')
            description = request.POST.get('description')
            equipments_used = request.POST.get('equipments_used')
            cost = request.POST.get('cost')

            # Validate start and end times
            start_time = datetime.strptime(start_time_str, '%H:%M').time()
            end_time = datetime.strptime(end_time_str, '%H:%M').time()

            if start_time >= end_time:
                return JsonResponse({'success': False, 'message': 'Start time must be greater than end time.'})

            # Calculate duration in hours
            duration = (datetime.combine(datetime.today(), end_time) - datetime.combine(datetime.today(), start_time)).seconds / 3600

            # Save procedure record
            procedure_record = Procedure.objects.create(
                patient=Patients.objects.get(mrn=mrn),
                name=name,
                description=description,
                duration_time=duration,
                equipments_used=equipments_used,
                cost=cost
            )

            return JsonResponse({'success': True, 'message': f'Procedure record for {procedure_record.name} saved successfully.'})
        except Patients.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Invalid patient ID.'})
        except IntegrityError:
            return JsonResponse({'success': False, 'message': 'Duplicate entry. Procedure record not saved.'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': f'An error occurred: {e}'})

    return JsonResponse({'success': False, 'message': 'Invalid request method.'})


@csrf_exempt  # Use csrf_exempt decorator for simplicity in this example. For a production scenario, consider using csrf protection.
def save_referral(request):
    if request.method == 'POST':
        try:
            mrn = request.POST.get('mrn')            
            source_location = request.POST.get('source_location')
            destination_location = request.POST.get('destination_location')
            reason = request.POST.get('reason')
            notes = request.POST.get('notes')       


            # Save procedure record
            referral_record = Referral.objects.create(
                patient=Patients.objects.get(mrn=mrn),
                source_location=source_location,
                destination_location=destination_location,
                reason=reason,
                notes=notes,
       
            )

            return JsonResponse({'success': True, 'message': f'Referral record for {referral_record} saved successfully.'})
        except Patients.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Invalid patient ID.'})
        except IntegrityError:
            return JsonResponse({'success': False, 'message': 'Duplicate entry. Referral record not saved.'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': f'An error occurred: {e}'})

    return JsonResponse({'success': False, 'message': 'Invalid request method.'})

@csrf_exempt
def change_referral_status(request):
    if request.method == 'POST':
        try:
            referral_id = request.POST.get('referralId')
            new_status = request.POST.get('newStatus')
            print(new_status)
            # Update referral record with new status
            referral_record = Referral.objects.get(id=referral_id)
            referral_record.status = new_status
            referral_record.save()

            return JsonResponse({'success': True, 'message': f'Status for {referral_record} changed successfully.'})
        except Referral.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Invalid Referral ID.'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': f'An error occurred: {e}'})

    return JsonResponse({'success': False, 'message': 'Invalid request method.'})

def manage_referral(request):
    referrals = Referral.objects.all()
    patients = Patients.objects.all()
    return render(request, 'hod_template/manage_referral.html', {'referrals': referrals,'patients':patients})


def generate_billing(request, procedure_id):
    procedure = get_object_or_404(Procedure, id=procedure_id)

    context = {
        'procedure': procedure,
    }

    return render(request, 'hod_template/billing_template.html', context)

def appointment_list_view(request):
    appointments = Consultation.objects.all()
    unread_notification_count = Notification.objects.filter(is_read=False).count()
    patients=Patients.objects.all() 
    pathology_records=PathodologyRecord.objects.all() 
    doctors=Staffs.objects.filter(role='doctor')
    context = {
        'patients':patients,
        'pathology_records':pathology_records,
        'doctors':doctors,
        'unread_notification_count':unread_notification_count,
        'appointments':appointments,
    }
    return render(request, 'hod_template/manage_appointment.html', context)

def import_staff(request):
    if request.method == 'POST':
        form = ImportStaffForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                staff_resource = StaffResources()
                new_staffs = request.FILES['staff_file']
                
                # Use tablib to load the imported data
                dataset = Dataset()
                imported_data = dataset.load(new_staffs.read(), format='xlsx')  # Assuming you are using xlsx, adjust accordingly

                for data in imported_data:
                   
                    user = CustomUser.objects.create_user(username=data[2],
                                                          password=data[2], 
                                                          email=data[2], 
                                                          first_name=data[0],
                                                          last_name=data[1],
                                                          user_type=2)
                    user.staff.middle_name =data[3],
                    user.staff.date_of_birth = data[5]
                    user.staff.gender = data[4],           
                    user.staff.phone_number = data[8]            
                    user.staff.marital_status = data[6]
                    user.staff.profession = data[7]
                    user.staff.role =data[9]
                    user.save()

                messages.success(request, 'Staff data imported successfully!')
            except Exception as e:
                messages.error(request, f'An error occurred: {e}')

    else:
        form = ImportStaffForm()

    return render(request, 'hod_template/import_staff.html', {'form': form})

@csrf_exempt
@login_required
def add_disease(request):
    try:
        if request.method == 'POST':
            disease_name = request.POST.get('Disease')
            code = request.POST.get('Code')

            # Save data to the model
            DiseaseRecode.objects.create(disease_name=disease_name, code=code)

            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'error': 'Invalid request method'})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})
 
@csrf_exempt
@login_required    
def add_insurance_company(request):
    try:
        if request.method == 'POST':
            name = request.POST.get('Name')
            phone = request.POST.get('Phone')
            short_name = request.POST.get('Short_name')
            email = request.POST.get('Email')
            address = request.POST.get('Address')

            # Save data to the model
            InsuranceCompany.objects.create(
                name=name,
                phone=phone,
                short_name=short_name,
                email=email,
                address=address
            )

            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'error': 'Invalid request method'})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})    
 
@csrf_exempt
@login_required      
def add_company(request):
    try:
        if request.method == 'POST':
            name = request.POST.get('Name')
            code = request.POST.get('Code')
            category = request.POST.get('Category')

            # Save data to the model
            Company.objects.create(
                name=name,
                code=code,
                category=category
            )

            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'error': 'Invalid request method'})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})
 
@csrf_exempt
@login_required
def add_pathodology_record(request):
    try:
        if request.method == 'POST':
            name = request.POST.get('Name')
            description = request.POST.get('Description')
            related_diseases_ids = request.POST.getlist('RelatedDiseases')

            # Save data to the model
            pathodology_record = PathodologyRecord.objects.create(
                name=name,
                description=description
            )

            # Add related diseases
            for disease_id in related_diseases_ids:
                disease = DiseaseRecode.objects.get(pk=disease_id)
                pathodology_record.related_diseases.add(disease)

            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'error': 'Invalid request method'})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})
    

@csrf_exempt
def add_patient(request):
    try:
        if request.method == 'POST':
            # Extract data from the request
            fullname = request.POST.get('fullname')
            email = request.POST.get('email')
            dob = request.POST.get('dob')
            gender = request.POST.get('gender')
            phone = request.POST.get('phone')
            address = request.POST.get('Address')
            nationality = request.POST.get('profession')            
            marital_status = request.POST.get('maritalStatus')
            patient_type = request.POST.get('patient_type')
            payment_type = request.POST.get('payment_type')
            insurance_name = request.POST.get('insurance_name')
            insurance_number = request.POST.get('insurance_number')
           

            # Generate the medical record number (mrn)
            mrn = generate_mrn()

            # Create an instance of the Patient model
            patient_instance = Patients(
                mrn=mrn,
                fullname=fullname,
                email=email,
                dob=dob,
                gender=gender,
                phone=phone,
                address=address,
                nationality=nationality,                
                marital_status=marital_status,
                patient_type=patient_type,
                payment_form=payment_type,
            )

            # If payment type is insurance, save insurance details
            if payment_type == 'insurance':
                patient_instance.insurance_name = insurance_name
                patient_instance.insurance_number = insurance_number
               

            # Save the instance to the database
            patient_instance.save()

            # Return a JsonResponse with a success message
            return JsonResponse({'message': 'Patient added successfully'}, status=200)

    except Exception as e:
        # Log or print the error for tracking
        logger.error(f"Error adding patient: {str(e)}")

    # Return an error response if there's an exception or if the request method is not POST
    return JsonResponse({'error': 'Failed to add patient'}, status=500)

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
      
      
@csrf_exempt
def add_medication_payment(request):
    if request.method == 'POST':
        try:
            # Extract data from the POST request
            patient_mrn = request.POST.get('mrn')
            non_registered_patient_name = request.POST.get('non_registered_patient_name')
            non_registered_patient_email = request.POST.get('non_registered_patient_email')
            non_registered_patient_phone = request.POST.get('non_registered_patient_phone')
            medicine_id = request.POST.get('medicine')
            medicine_used = int(request.POST.get('quantity'))
            amount = request.POST.get('amount')
            payment_date = request.POST.get('payment_date')

     
            
            patient = Patients.objects.get(mrn=patient_mrn) if patient_mrn else None
            medicine = Medicine.objects.get(id=medicine_id)
            
            # Check if there is sufficient stock
            medicine_inventory = medicine.medicineinventory_set.first()
            if medicine_inventory and medicine_used > medicine_inventory.remain_quantity:
                 return JsonResponse({'success': False, 'message': f'Insufficient stock. Only {medicine_inventory.remain_quantity} {medicine.name} available.'})
            # Create MedicationPayment instance
            medication_payment = MedicationPayment(
                patient=patient,
                non_registered_patient_name=non_registered_patient_name,
                non_registered_patient_email=non_registered_patient_email,
                non_registered_patient_phone=non_registered_patient_phone,
                medicine=medicine,
                quantity=medicine_used,
                amount=amount,
                payment_date=payment_date,
            )
            medication_payment.save()          

            return JsonResponse({'success': True, 'message': f'MedicationPayment record for {medication_payment} saved successfully.'})
        except Patients.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Invalid patient ID.'})
        except IntegrityError:
            return JsonResponse({'success': False, 'message': 'Duplicate entry.  record not saved.'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': f'An error occurred: {e}'})

    return JsonResponse({'error': 'Invalid request method'}, status=400)

     

@require_POST
@csrf_exempt
def delete_medication_payment(request, payment_id):
    try:
        # Retrieve the MedicationPayment instance
        medication_payment = MedicationPayment.objects.get(pk=payment_id)

        # Get the related MedicineInventory entry
        inventory_entry = medication_payment.medicine.medicineinventory

        # Update the inventory to reverse the impact of the MedicationPayment
        inventory_entry.quantity += medication_payment.quantity
        inventory_entry.amount -= medication_payment.amount

        # Save the updated inventory entry
        inventory_entry.save()

        # Delete the MedicationPayment
        medication_payment.delete()

        return JsonResponse({'message': 'Medication Payment deleted successfully'})
    except MedicationPayment.DoesNotExist:
        return JsonResponse({'error': 'Medication Payment not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
    

def medication_payments_view(request):
    # Subquery to retrieve the latest medication payment record for each registered patient
    latest_medication_payment = MedicationPayment.objects.filter(
        patient=OuterRef('id')
    ).order_by('-payment_date')[:1]

    # Query to retrieve medication payments for registered patients
    unique_patients_medication = Patients.objects.annotate(
        quantity=Subquery(latest_medication_payment.values('quantity')[:1]),
        amount=Subquery(latest_medication_payment.values('amount')[:1]),
        payment_date=Subquery(latest_medication_payment.values('payment_date')[:1]),
        medicine=Subquery(latest_medication_payment.values('medicine__name')[:1]),
    ).filter(quantity__isnull=False)

    # Additional filtering for medicines with enough quantity and not expired
    current_date = timezone.now().date()
    medicines_with_inventory = MedicineInventory.objects.filter(
        remain_quantity__gt=0,
        medicine__expiration_date__gt=current_date
    ).values('medicine')
    
    medicines = Medicine.objects.filter(id__in=medicines_with_inventory)

    # Retrieve the data
    data = unique_patients_medication.values(
        'id', 'mrn', 'medicine',
        'quantity', 'amount','payment_date'       
    )
    patients = Patients.objects.all()
    context = {
        'data': data,
        'medicines': medicines,
        'patients': patients,
    }

    return render(request, 'hod_template/manage_medication_payment.html', context)

def patient_medicationpayment_history_view(request, mrn):
    # Retrieve medication payment history for the patient with the given MRN
    medication_history = MedicationPayment.objects.filter(patient__mrn=mrn)
    
        # Additional filtering for medicines with enough quantity and not expired
    current_date = timezone.now().date()
    medicines_with_inventory = MedicineInventory.objects.filter(
        quantity__gt=100,
        medicine__expiration_date__gt=current_date
    ).values('medicine')
    
    medicines = Medicine.objects.filter(id__in=medicines_with_inventory)
    context = {'medication_history': medication_history, 'mrn': mrn,'medicines':medicines}
    return render(request, 'hod_template/manage_patient_medicationpayment_history.html', context)


def diagnostic_tests_view(request):
    # Retrieve all diagnostic tests from the database
    diagnostic_tests = DiagnosticTest.objects.all()

    # Retrieve patients, diseases, health issues, and pathologies
    patients = Patients.objects.all()
    diseases = DiseaseRecode.objects.all()
    health_issues = HealthIssue.objects.all()
    pathologies = PathodologyRecord.objects.all()

    context = {
        'diagnostic_tests': diagnostic_tests,
        'patients': patients,
        'diseases': diseases,
        'health_issues': health_issues,
        'pathologies': pathologies,
    }

    return render(request, 'hod_template/manage_diagnostic_tests.html', context)


def save_diagnostic_test(request):
    if request.method == 'POST':
        try:
            # Retrieve form data from POST request
            patient_id = request.POST.get('patient')
            test_type = request.POST.get('test_type')
            test_date = request.POST.get('test_date')
            result = request.POST.get('result')
            disease_or_pathology = request.POST.get('disease_or_pathology')   
              
            patient_id = request.POST.get('patient')
            
            pathology_id = None
            diseases_ids = None
            health_issues_ids = None
            if disease_or_pathology == 'pathology':
                pathology_id = request.POST.get('Disease_Pathology_otherhealthissues')
                
            if disease_or_pathology == 'disease':
                diseases_ids = request.POST.get('Disease_Pathology_otherhealthissues')                
            if disease_or_pathology == 'health_issue':
                health_issues_ids = request.POST.get('Disease_Pathology_otherhealthissues')
            # Convert test_date to a valid date object (you may need to adjust the format)
            # test_date = datetime.datetime.strptime(test_date, '%Y-%m-%d').date()
            test_id = generate_test_id()
            # Create a new DiagnosticTest object
            diagnostic_test = DiagnosticTest(
                test_id=test_id,
                patient_id=patient_id,
                test_type=test_type,
                test_date=test_date,
                result=result,
                pathology_record_id=pathology_id
            )

            diagnostic_test.save()

            # Add diseases and health issues to the many-to-many fields
            if diseases_ids is not None:
                diagnostic_test.diseases.set(diseases_ids)
                
            if health_issues_ids is not None:
               diagnostic_test.health_issues.set(health_issues_ids)

            # Redirect to a success page or another appropriate URL
            return redirect('diagnostic_tests')  # Adjust the URL as needed

        except Exception as e:
            print(f"ERROR: {str(e)}")
            return HttpResponseBadRequest(f"Error: {str(e)}")

    return HttpResponseBadRequest("Invalid request method")

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

def sample_list(request):
    samples = Sample.objects.all()
    diagnostic_tests = DiagnosticTest.objects.all()    
    return render(request, 'hod_template/manage_sample_list.html', {'samples': samples,'diagnostic_tests':diagnostic_tests})


def save_sample(request):
    if request.method == 'POST':
        try:
            # Retrieve form data from POST request
            lab_test = request.POST.get('lab_test')
            collection_date = request.POST.get('collection_date')   
                      # Create a new Sample object
            sample = Sample(
                lab_test= DiagnosticTest.objects.get(id=lab_test),  # Replace with the actual instance
                collection_date=collection_date,               
             
            )

            sample.save()

            # Redirect to a success page or another appropriate URL
            return redirect('sample_list')  # Adjust the URL as needed

        except Exception as e:
            print(f"ERROR: {str(e)}")
            return HttpResponseBadRequest(f"Error: {str(e)}")

    return HttpResponseBadRequest("Invalid request method")


def patient_diseases_view(request):
    # Retrieve all diagnostic tests from the database
    patient_diseases = PatientDisease.objects.all()

    # Retrieve patients, diseases
    patients = Patients.objects.all()
    diseases = DiseaseRecode.objects.all()


    context = {
        'patient_diseases': patient_diseases,
        'patients': patients,
        'disease_records': diseases,
      
    }

    return render(request, 'hod_template/manage_patient_disease_list.html', context)

def save_patient_disease(request):
    if request.method == 'POST':
        try:
            # Extract data from the POST request
            patient_id = request.POST.get('patient_id')
            disease_record_id = request.POST.get('diseaseRecord')
            diagnosis_date = request.POST.get('diagnosisDate')
            severity = request.POST.get('severity')
            treatment_plan = request.POST.get('treatmentPlan')

            # Validate data (add more validation as needed)
            if not patient_id or not disease_record_id or not diagnosis_date:
                return JsonResponse({'status': 'error', 'message': 'Incomplete data received'}, status=400)

            # Convert data types if needed (e.g., converting string to datetime)
            # ...

            # Create a PatientDisease instance and save to the database
            patient_disease = PatientDisease.objects.create(
                patient_id=patient_id,
                disease_record_id=disease_record_id,
                diagnosis_date=diagnosis_date,
                severity=severity,
                treatment_plan=treatment_plan,
            )

            # You can include additional logic here if needed

            return redirect('patient_diseases_view') 
        except Exception as e:
            print(f"ERROR: {str(e)}")
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

    # If the request method is not POST, redirect to an appropriate page
    return HttpResponseBadRequest("Invalid request method") 

def pathology_diagnostic_test_list(request):
    Pathology_diagnostic_tests = PathologyDiagnosticTest.objects.all()
    pathology_records=PathodologyRecord.objects.all() 
    diagnostic_tests = DiagnosticTest.objects.all()
    return render(request, 'hod_template/manage_pathology_diagnostic_test_list.html', {
        'Pathology_diagnostic_tests': Pathology_diagnostic_tests,
        'pathology_records': pathology_records,
        'diagnostic_tests': diagnostic_tests,
        }) 

def pathology_diagnostic_test_save(request):
    if request.method == 'POST':
        try:
            # Retrieve data from the form
            pathology_record_id = request.POST.get('pathologyRecord')
            diagnostic_test_id = request.POST.get('diagnosticTest')
            test_result = request.POST.get('testResult')
            testing_date = request.POST.get('testingDate')
            conducted_by = request.POST.get('conductedBy')

            # Create PathologyDiagnosticTest instance
            pathology_diagnostic_test = PathologyDiagnosticTest.objects.create(
                pathology_record_id=pathology_record_id,
                diagnostic_test_id=diagnostic_test_id,
                test_result=test_result,
                testing_date=testing_date,
                conducted_by=conducted_by
            )

            # Optionally, you can perform additional actions or redirect to another page
            return redirect('pathology_diagnostic_test_list') 

        except Exception as e:
            # Handle exceptions (e.g., invalid data, database errors)
            return HttpResponseBadRequest(f"Error: {str(e)}")

    else:
        # Handle non-POST requests if needed
        return HttpResponseBadRequest("Invalid request method.")



@require_POST
def save_consultation_data(request):
    try:
        # Retrieve data from the form
        doctor_id = request.POST.get('doctor')
        patient_id = request.POST.get('patient')
        appointment_date = request.POST.get('appointmentDate')
        start_time = request.POST.get('startTime')
        end_time = request.POST.get('endTime')
        description = request.POST.get('description')        
        pathodology_record_id = request.POST.get('pathodologyRecord')

        # Convert date and time strings to datetime objects
        # appointment_datetime = datetime.combine(datetime.strptime(appointment_date, '%Y-%m-%d').date(), datetime.strptime(start_time, '%H:%M').time())
        # end_datetime = datetime.combine(datetime.strptime(appointment_date, '%Y-%m-%d').date(), datetime.strptime(end_time, '%H:%M').time())

        # Create or update Consultation object
        consultation, created = Consultation.objects.update_or_create(
            doctor=Staffs.objects.get(id=doctor_id),
            patient=Patients.objects.get(id=patient_id),
            appointment_date=appointment_date,
            start_time=start_time,
            end_time=end_time,
            description=description,
            pathodology_record= PathodologyRecord.objects.get(id=pathodology_record_id),
            
        )

        return redirect('appointment_list')
    except Exception as e:
        return HttpResponseBadRequest(f"Error: {str(e)}")

def consultation_fee_list(request):
    # Get distinct patients who have consultations
    patients = Patients.objects.filter(consultation__isnull=False).distinct()

    # Get distinct doctors who have consultations
    doctors = Staffs.objects.filter(consultation__isnull=False).distinct()

    # Get all consultation fees
    consultation_fees = ConsultationFee.objects.all()

    # Get all consultations
    consultations = Consultation.objects.all()

    return render(request, 'hod_template/manage_consultation_fee_list.html', {
        'consultation_fees': consultation_fees,
        'patients': patients,
        'doctors': doctors,
        'consultations': consultations,
    })

@require_POST
def save_consultation_fee(request):
    try:
        # Extract form data from the request
        doctor_id = request.POST.get('doctor')
        patient_id = request.POST.get('patient')
        fee_amount = request.POST.get('feeAmount')
        consultation_id = request.POST.get('consultation')

        # Create ConsultationFee instance
        consultation_fee = ConsultationFee.objects.create(
            doctor=Staffs.objects.get(id=doctor_id),
            patient=Patients.objects.get(id=patient_id),
            fee_amount=fee_amount,
            consultation=Consultation.objects.get(id=consultation_id),
        )

        # Return a JsonResponse to indicate success
        return redirect('consultation_fee_list') 
    except Exception as e:
        # Return a JsonResponse with an error message
        return HttpResponseBadRequest(f"Error: {str(e)}")  
    
    
def save_service_data(request):
    if request.method == 'POST':
        service_id = request.POST.get('service_id')
        covarage = request.POST.get('covarage')
        department = request.POST.get('department')
        type_service = request.POST.get('typeService')
        name = request.POST.get('serviceName')
        description = request.POST.get('description')
        cost = request.POST.get('cost')

        try:
            if service_id:
                # Editing existing service
                service = Service.objects.get(pk=service_id)
            else:
                # Creating a new service
                service = Service()

            service.covarage = covarage
            service.department = department
            service.type_service = type_service
            service.name = name
            service.description = description
            service.cost = cost
            service.save()

            return redirect('manage_service')
        except Exception as e:
            return HttpResponseBadRequest(f"Error: {str(e)}") 

    # If the request is not a POST request, handle it accordingly
    return HttpResponseBadRequest("Invalid request method.")   

def category_list(request):
    categories = Category.objects.all()
    return render(request, 'hod_template/manage_category_list.html', {'categories': categories})


@require_POST
def add_category(request):
    try:
        category_id = request.POST.get('category_id')
        name = request.POST.get('name')
        # Add more fields as needed

        if category_id:
            # Editing an existing category
            category = Category.objects.get(pk=category_id)
            category.name = name
         
            category.save()
        else:
            # Adding a new category
            category = Category(name=name)
            category.save()

        return JsonResponse({'status': 'success'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)})
    
def supplier_list(request):
    suppliers = Supplier.objects.all()
    return render(request, 'hod_template/manage_supplier_list.html', {'suppliers': suppliers})
 
def inventory_list(request):
    inventory_items = InventoryItem.objects.all()  
    suppliers = Supplier.objects.all()
    categories = Category.objects.all()
    return render(request, 'hod_template/manage_inventory_list.html', {
        'inventory_items': inventory_items,
        'suppliers': suppliers,
        'categories': categories 
        }) 


@require_POST
def add_supplier(request):
    try:
        supplier_id = request.POST.get('supplier_id')
        name = request.POST.get('name')
        address = request.POST.get('address', '')
        contact_information = request.POST.get('contact_information', '')
        email = request.POST.get('email', '')

        if supplier_id:
            # Editing an existing supplier
            supplier = Supplier.objects.get(pk=supplier_id)
            supplier.name = name
            supplier.address = address
            supplier.contact_information = contact_information
            supplier.email = email         
            supplier.save()
        else:
            # Adding a new supplier
            supplier = Supplier(
                name=name,
                address=address,
                contact_information=contact_information,
                email=email,                
            )
            supplier.save()

        return JsonResponse({'status': 'success'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}) 
    

@require_POST
def add_inventory_item(request):
    try:
        inventory_id = request.POST.get('inventory_id')
        name = request.POST.get('name')
        supplier = request.POST.get('supplier')
        category = request.POST.get('category')
        quantity = int(request.POST.get('quantity'))
        description = request.POST.get('description')
        purchase_date = request.POST.get('purchase_date')
        purchase_price = request.POST.get('purchase_price')
        expiry_date = request.POST.get('expiry_date')
        min_stock_level = request.POST.get('min_stock_level')
        condition = request.POST.get('condition')
        location_in_storage = request.POST.get('location_in_storage')
        # Add more fields as needed

        if inventory_id:
            # Editing existing inventory item
            inventory_item = InventoryItem.objects.get(pk=inventory_id)
            inventory_item.name = name
            inventory_item.quantity = quantity
            inventory_item.remain_quantity = quantity
            inventory_item.category =  Category.objects.get(id=category)
            inventory_item.description = description
            inventory_item.supplier =  Supplier.objects.get(id=supplier)
            inventory_item.purchase_date = purchase_date
            inventory_item.purchase_price = purchase_price
            inventory_item.location_in_storage = location_in_storage
            inventory_item.min_stock_level = min_stock_level
            inventory_item.expiry_date = expiry_date
            inventory_item.condition = condition
            inventory_item.save()
        else:
            # Adding new inventory item
            inventory_item = InventoryItem(
                name=name,
                quantity=quantity,
                remain_quantity=quantity,
                category = Category.objects.get(id=category),
                description = description,
                supplier = Supplier.objects.get(id=supplier),
                purchase_date = purchase_date,
                purchase_price = purchase_price,
                location_in_storage = location_in_storage,
                min_stock_level = min_stock_level,
                expiry_date = expiry_date,
                condition = condition,
               
            )
            inventory_item.save()

        return JsonResponse({'status': 'success'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)})      
    

def usage_history_list(request):
    usage_history_list = UsageHistory.objects.filter(quantity_used__gt=0)
    inventory_item = InventoryItem.objects.all()
    return render(request, 'hod_template/manage_usage_history_list.html', {
        'usage_history_list': usage_history_list,
        'inventory_item': inventory_item,
        })    

@require_POST
def save_usage_history(request):
    try:
        # Extract data from the request
        usage_history_id = request.POST.get('usageHistoryId')
        usage_date = request.POST.get('usageDate')
        quantity_used = int(request.POST.get('quantityUsed'))
        notes = request.POST.get('notes')
        item_id = request.POST.get('item')

        # Retrieve the corresponding InventoryItem
        item = InventoryItem.objects.get(id=item_id)
        if quantity_used > item.remain_quantity:
            return JsonResponse({'status': 'error', 'message': 'Quantity used exceeds available stock quantity'})


        # Check if the usageHistoryId is provided for editing
        if usage_history_id:
            # Editing existing usage history
            usage_history = UsageHistory.objects.get(pk=usage_history_id)
            # Get the previous quantity used
            previous_quantity_used = usage_history.quantity_used
            # Calculate the difference in quantity
            quantity_difference = quantity_used - previous_quantity_used
            # Update the stock level of the corresponding item
            item.remain_quantity -= quantity_difference
        else:
            # Creating new usage history
            usage_history = UsageHistory()
         

        # Update or set values for other fields
        usage_history.usage_date = usage_date
        usage_history.quantity_used = quantity_used
        usage_history.notes = notes
        usage_history.inventory_item = item

        # Save the changes to both models
        item.save()
        usage_history.save()

        return JsonResponse({'status': 'success'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)})

@csrf_exempt
def get_item_quantity(request):
    if request.method == 'POST':
        item_id = request.POST.get('itemId')  # Use request.POST.get() instead of request.GET.get()
        print(item_id)      
        try:
            item = InventoryItem.objects.get(id=item_id)
            quantity = item.quantity
            print(quantity)
            return JsonResponse({'quantity': quantity})
        except InventoryItem.DoesNotExist:
            return JsonResponse({'error': 'Item not found'}, status=404)
    else:
        return JsonResponse({'error': 'Invalid request'}, status=400)
    

def out_of_stock_items(request):
    out_of_stock_items = InventoryItem.objects.filter(remain_quantity=0)
    return render(request, 'hod_template/manage_out_of_stock_items.html', {'out_of_stock_items': out_of_stock_items}) 

def in_stock_items(request):
    in_stock_items = InventoryItem.objects.filter(remain_quantity__gt=0)
    return render(request, 'hod_template/manage_in_stock_items.html', {'in_stock_items': in_stock_items})   

def get_out_of_stock_count(request):
    count = InventoryItem.objects.filter(remain_quantity=0).count()
    
    return JsonResponse({'count': count})

def get_out_of_stock_count_reagent(request):
    count = Reagent.objects.filter(remaining_quantity=0).count()
    
    return JsonResponse({'count': count})

def get_items_below_min_stock(request):
    items_below_min_stock = InventoryItem.objects.filter(remain_quantity__lt=F('min_stock_level')).count()
    return JsonResponse({'count': items_below_min_stock})

@csrf_exempt
def increase_inventory_stock(request):
    if request.method == 'POST':
        item_id = request.POST.get('item_id')
        quantity_to_add = int(request.POST.get('quantityToAdd'))
        try:
            item = InventoryItem.objects.get(id=item_id)
            item.quantity += quantity_to_add
            item.remain_quantity += quantity_to_add
            item.save()
            return JsonResponse({'status': 'success', 'message': f'Stock level increased by {quantity_to_add} for item {item.name}'})
        except InventoryItem.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Item not found'}, status=404)
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)
    
@csrf_exempt
def increase_reagent_stock(request):
    if request.method == 'POST':
        reagent_id = request.POST.get('reagent_id')
        quantity_to_add = int(request.POST.get('quantityToAdd'))
        try:
            reagent = Reagent.objects.get(id=reagent_id)
            reagent.quantity_in_stock += quantity_to_add
            reagent.remaining_quantity += quantity_to_add
            reagent.save()
            return JsonResponse({'status': 'success', 'message': f'Stock level increased by {quantity_to_add} for item {reagent.name}'})
        except InventoryItem.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Item not found'}, status=404)
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)

@csrf_exempt    
def use_inventory_item(request):
    if request.method == 'POST':
        item_id = request.POST.get('itemId')
        notes = request.POST.get('notes')
        quantity_used = int(request.POST.get('quantityUsed'))
        usage_date = request.POST.get('usageDate')

        try:
            item = InventoryItem.objects.get(id=item_id)
            if quantity_used > item.remain_quantity:
                return JsonResponse({'status': 'error', 'message': 'Quantity used exceeds available stock quantity'})

            # Create a new usage history entry
            UsageHistory.objects.create(
                inventory_item=item,
                quantity_used=quantity_used,
                notes=notes,
                usage_date=usage_date
            )

            item.remain_quantity -= quantity_used
            item.save()

            message = f'Stock level decreased by {quantity_used} for item {item.name}'
            return JsonResponse({'status': 'success', 'message': message})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})

    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request'})
    
def out_of_stock_medicines(request):
    try:
        # Query the database for the count of out-of-stock medicines
        out_of_stock_count = MedicineInventory.objects.filter(remain_quantity=0).count()
        
        # Return the count in JSON format
        return JsonResponse({'count': out_of_stock_count})
    
    except Exception as e:
        # Handle any errors and return an error response
        return JsonResponse({'error': str(e)}, status=500)    
    
def out_of_stock_medicines_view(request):
    try:
        # Query the database for out-of-stock medicines
        out_of_stock_medicines = MedicineInventory.objects.filter(remain_quantity=0)
        
        # Render the template with the out-of-stock medicines data
        return render(request, 'hod_template/manage_out_of_stock_medicines.html', {'out_of_stock_medicines': out_of_stock_medicines})
    
    except Exception as e:
        # Handle any errors and return an error response
        return render(request, 'error.html', {'error_message': str(e)}) 
    
def out_of_stock_reagent_view(request):
    try:
        # Query the database for out-of-stock medicines
        out_of_stock_reagent = Reagent.objects.filter(remaining_quantity=0)
        
        # Render the template with the out-of-stock medicines data
        return render(request, 'hod_template/manage_out_of_stock_reagent.html', {'out_of_stock_reagent': out_of_stock_reagent})
    
    except Exception as e:
        # Handle any errors and return an error response
        return render(request, 'error.html', {'error_message': str(e)}) 
    
    
def in_stock_medicines_view(request):
    # Retrieve medicines with inventory levels above zero
    in_stock_medicines = MedicineInventory.objects.filter(remain_quantity__gt=0)

    return render(request, 'hod_template/manage_in_stock_medicines.html', {'in_stock_medicines': in_stock_medicines})  

def in_stock_reagent_view(request):
    # Retrieve medicines with inventory levels above zero
    in_stock_reagent = Reagent.objects.filter(remaining_quantity__gt=0)

    return render(request, 'hod_template/manage_in_stock_reagent.html', {'in_stock_reagent': in_stock_reagent})  

def equipment_list(request):
    equipment_list = Equipment.objects.all()
    return render(request, 'hod_template/manage_equipment_list.html', {'equipment_list': equipment_list})  

 
@csrf_exempt     
@require_POST
def add_equipment(request):
    try:
        equipment_id = request.POST.get('equipment_id')
        Manufacturer = request.POST.get('Manufacturer')
        SerialNumber = request.POST.get('SerialNumber')
        AcquisitionDate = request.POST.get('AcquisitionDate')
        warrantyExpiryDate = request.POST.get('warrantyExpiryDate')
        Location = request.POST.get('Location')
        description = request.POST.get('description')
        Name = request.POST.get('Name')
      
        # Add more fields as needed

        if equipment_id:
            # Editing existing inventory item
            equipment = Equipment.objects.get(pk=equipment_id)
            equipment.manufacturer = Manufacturer
            equipment.serial_number = SerialNumber
            equipment.acquisition_date = AcquisitionDate
            equipment.warranty_expiry_date =  warrantyExpiryDate
            equipment.description = description
            equipment.location = Location
            equipment.name = Name        
            equipment.save()
        else:
            # Adding new inventory item
            equipment = Equipment(
                name=Name,
                manufacturer=Manufacturer,
                serial_number=SerialNumber,
                acquisition_date = AcquisitionDate,
                description = description,
                warranty_expiry_date = warrantyExpiryDate,
                location = Location,             
               
            )
            equipment.save()

        return JsonResponse({'status': 'success'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)})  
    
    
def equipment_maintenance_list(request):
    maintenance_list = EquipmentMaintenance.objects.all()
    equipments = Equipment.objects.all()
    return render(request, 'hod_template/manage_equipment_maintenance_list.html',
                  {
                      'maintenance_list': maintenance_list,
                      'equipments': equipments,
                   })    

@csrf_exempt     
@require_POST
def add_maintainance(request):
    try:
        maintenance_id = request.POST.get('maintenance_id')
        equipment = request.POST.get('equipment')
        maintenance_date = request.POST.get('maintenance_date')
        technician = request.POST.get('technician')
        description = request.POST.get('description')
        cost = request.POST.get('cost')
        notes = request.POST.get('notes')
      
      
        # Add more fields as needed

        if maintenance_id:
            # Editing existing inventory item
            maintainance = EquipmentMaintenance.objects.get(pk=maintenance_id)
            maintainance.equipment = Equipment.objects.get(id=equipment)
            maintainance.maintenance_date = maintenance_date
            maintainance.technician = technician
            maintainance.description =  description
            maintainance.cost = cost
            maintainance.notes = notes                    
            maintainance.save()
        else:
            # Adding new inventory item
            maintainance = EquipmentMaintenance(
                equipment= Equipment.objects.get(id=equipment),
                maintenance_date=maintenance_date,
                technician=technician,
                description = description,
                cost = cost,
                notes = notes,
                          
               
            )
            maintainance.save()

        return JsonResponse({'status': 'success'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)})  
 
def reagent_list(request):
    reagent_list = Reagent.objects.all()
    return render(request, 'hod_template/manage_reagent_list.html', {'reagent_list': reagent_list})    

@csrf_exempt     
@require_POST
def add_reagent(request):
    try:
        reagent_id = request.POST.get('reagent_id')
        name = request.POST.get('name')
        expiration_date = request.POST.get('expiration_date')
        manufacturer = request.POST.get('manufacturer')
        lot_number = request.POST.get('lot_number')
        storage_conditions = request.POST.get('storage_conditions')
        quantity_in_stock = int(request.POST.get('quantity_in_stock'))
        price_per_unit = float(request.POST.get('price_per_unit'))
      
      
        # Add more fields as needed

        if reagent_id:
            # Editing existing inventory item
            reagent = Reagent.objects.get(pk=reagent_id)
            reagent.name = name
            reagent.expiration_date = expiration_date
            reagent.manufacturer = manufacturer
            reagent.lot_number =  lot_number
            reagent.storage_conditions = storage_conditions
            reagent.quantity_in_stock = quantity_in_stock                    
            reagent.price_per_unit = price_per_unit                    
            reagent.remaining_quantity = quantity_in_stock                    
            reagent.save()
        else:
            # Adding new inventory item
            reagent = Reagent(
                name=name,
                expiration_date=expiration_date,
                manufacturer=manufacturer,
                lot_number = lot_number,
                storage_conditions = storage_conditions,
                quantity_in_stock = quantity_in_stock,
                price_per_unit = price_per_unit,
                remaining_quantity = quantity_in_stock,
                          
               
            )
            reagent.save()

        return JsonResponse({'status': 'success'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)})  

def reagent_usage_list(request):
    reagent_usage_list = ReagentUsage.objects.all()
    technicians = Staffs.objects.all()
    reagents = Reagent.objects.all()
    return render(request, 'hod_template/manage_reagent_usage_list.html',
                  {
                      'reagent_usage_list': reagent_usage_list,
                      'technicians': technicians,
                      'reagents': reagents,
                   }
                  )

@csrf_exempt
@require_POST
def add_reagent_used(request):
    try:
        # Extract data from the request
        usage_id = request.POST.get('usage_id')
        labTechnician = request.POST.get('labTechnician')
        reagent_id = request.POST.get('reagent')
        usage_date = request.POST.get('usage_date')
        quantity_used = int(request.POST.get('quantity_used'))
        observation = request.POST.get('observation')
        technician_notes = request.POST.get('technician_notes')

        # Retrieve the corresponding InventoryItem
        labTechnician = Staffs.objects.get(id=labTechnician)
        reagent = Reagent.objects.get(id=reagent_id)
        
        if quantity_used > reagent.remaining_quantity:
            return JsonResponse({'status': 'error', 'message': 'Quantity used exceeds available stock quantity'})


        # Check if the usageHistoryId is provided for editing
        if usage_id:
            # Editing existing usage history
            usage_history = ReagentUsage.objects.get(pk=usage_id)
            # Get the previous quantity used
            previous_quantity_used = usage_history.quantity_used
            # Calculate the difference in quantity
            quantity_difference = quantity_used - previous_quantity_used
            # Update the stock level of the corresponding item
            reagent.remaining_quantity -= quantity_difference
        else:
            # Creating new usage history
            usage_history = ReagentUsage()
         

        # Update or set values for other fields
        usage_history.lab_technician = labTechnician
        usage_history.usage_date = usage_date
        usage_history.quantity_used = quantity_used
        usage_history.technician_notes = technician_notes
        usage_history.reagent = reagent
        usage_history.observation = observation

        # Save the changes to both models
        reagent.save()
        usage_history.save()

        return JsonResponse({'status': 'success'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)})
    
@csrf_exempt
@require_POST
def add_prescription(request):
    try:
        # Extract data from the request
        prescription_id = request.POST.get('prescription_id')
        patient_id = request.POST.get('patient')
        medicine_id = request.POST.get('medicine')
        route = request.POST.get('route')
        medicine_used = int(request.POST.get('quantity'))
        frequency = request.POST.get('frequency')
        duration = request.POST.get('duration')
        dose = request.POST.get('dose')

        # Retrieve the corresponding patient and medicine
        patient = Patients.objects.get(id=patient_id)
        medicine = Medicine.objects.get(id=medicine_id)
        
        # Check if there is sufficient stock
        medicine_inventory = medicine.medicineinventory_set.first()
        if medicine_inventory and medicine_used > medicine_inventory.remain_quantity:
            return JsonResponse({'success': False, 'message': f'Insufficient stock. Only {medicine_inventory.remain_quantity} {medicine.name} available.'})

        # Check if the usageHistoryId is provided for editing
        if prescription_id:
            # Editing existing prescription
            prescription = Prescription.objects.get(pk=prescription_id)
            # Get the previous quantity used
            previous_quantity_used = prescription.quantity_used
            
            # Calculate the difference in quantity
            quantity_difference = medicine_used - previous_quantity_used
            
            # Update the stock level of the corresponding item
            if medicine_inventory:
                medicine_inventory.remain_quantity -= quantity_difference
                medicine_inventory.save()
            # Recalculate total price
            total_price = medicine_used * medicine.unit_price
            prescription.total_price = total_price
        else:
            # Creating new prescription
            prescription = Prescription()
            prs_no = generate_prescription_id()
            prescription.prs_no = prs_no

        # Update or set values for other fields
        prescription.patient = patient
        prescription.medicine = medicine
        prescription.route = route
        prescription.dose = dose
        prescription.frequency = frequency
        prescription.duration = duration
        prescription.quantity_used = medicine_used

        # Save the changes to both models
        prescription.save()

        return JsonResponse({'status': 'success'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)})    
    
def generate_prescription_id():
    last_prescription = Prescription.objects.last()
    last_sample_number = int(last_prescription.prs_no.split('-')[-1]) if last_prescription else 0
    new_prescription_id = last_sample_number + 1
    return f"PRS-{new_prescription_id:07d}"



    
    
def generate_remoteprescription_id():
    last_prescription = RemotePrescription.objects.last()
    last_sample_number = int(last_prescription.prs_no.split('-')[-1]) if last_prescription else 0
    new_prescription_id = last_sample_number + 1
    return f"PRS-{new_prescription_id:07d}"
    
def quality_control_list(request):
    # Retrieve all QualityControl objects
    quality_controls = QualityControl.objects.all()
    technicians = Staffs.objects.all()
    # Pass the queryset to the template for rendering
    return render(request, 'hod_template/manage_quality_control_list.html', 
                  {
                      'quality_controls': quality_controls,
                      'technicians': technicians,
                      }
                  ) 

@csrf_exempt     
@require_POST
def add_quality_control(request):
    try:
        qualitycontrol_id = request.POST.get('qualitycontrol_id')
        lab_technician = request.POST.get('lab_technician')
        control_date = request.POST.get('control_date')
        control_type = request.POST.get('control_type')
        result = request.POST.get('result')
        remarks = request.POST.get('remarks')

      
      
        # Add more fields as needed
        lab_technician = Staffs.objects.get(id=lab_technician)
        
        if qualitycontrol_id:
            # Editing existing inventory item
            reagent = QualityControl.objects.get(pk=qualitycontrol_id)
            reagent.lab_technician = lab_technician
            reagent.control_date = control_date
            reagent.control_type = control_type
            reagent.result =  result
            reagent.remarks = remarks
                            
            reagent.save()
        else:
            # Adding new inventory item
            reagent = QualityControl(
            lab_technician=lab_technician,
            control_date=control_date,
            control_type=control_type,
            result=result,
            remarks=remarks
                          
               
            )
            reagent.save()

        return JsonResponse({'status': 'success'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)})  
    
def health_issue_list(request):
    health_issues = HealthIssue.objects.all()
    return render(request, 'hod_template/manage_health_issues.html', {'health_issues': health_issues})       

@csrf_exempt     
@require_POST
def add_health_issue(request):
    try:
        health_id = request.POST.get('health_id')
        name = request.POST.get('name')
        description = request.POST.get('description')
        is_disease = request.POST.get('is_disease')
        severity = request.POST.get('severity')
        treatment_plan = request.POST.get('treatment_plan')
        onset_date = request.POST.get('onset_date')
        resolution_date = request.POST.get('resolution_date')

      
      
      
        
        if health_id:
            # Editing existing HealthIssue item
            health_issue = HealthIssue.objects.get(pk=health_id)
            health_issue.name = name
            health_issue.description = description
            health_issue.is_disease = bool(is_disease)
            health_issue.onset_date =  onset_date            
            health_issue.severity = severity
            health_issue.treatment_plan = treatment_plan
            health_issue.resolution_date = resolution_date
                            
            health_issue.save()
        else:
            # Adding new HealthIssue item
            health_issue = HealthIssue(
            name=name,
            description=description,
            is_disease=bool(is_disease),
            severity=severity,
            onset_date=onset_date,
            treatment_plan=treatment_plan,
            resolution_date=resolution_date
                          
               
            )
            health_issue.save()

        return JsonResponse({'status': 'success'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)})
    
     
@csrf_exempt     
@require_POST
def add_patient_visit(request):
    try:
        visit_id = request.POST.get('visit_id')
        visitType = request.POST.get('visitType')        
        insuranceName = request.POST.get('insuranceName')
        insuranceNumber = request.POST.get('insuranceNumber')
        verificationCode = request.POST.get('verificationCode')
        visitReason = request.POST.get('visitReason')
        patient_id = request.POST.get('patient_id')    
        referral_number = request.POST.get('visitReason')    
        primary_service = request.POST.get('primary_service')  
        
        patient = Patients.objects.get(pk=patient_id)
        if visit_id:
            # Editing existing HealthIssue item
            visit = PatientVisits.objects.get(pk=visit_id)
            visit.visit_type = visitType         
            visit.patient = patient
            visit.primary_service = primary_service
            visit.insurance_name = insuranceName
            visit.insurance_number =  insuranceNumber            
            visit.authorization_code = verificationCode
            visit.visit_reason = visitReason
            visit.referral_number = referral_number
                            
            visit.save()
        else:
            # Adding new PatientVisit item
            vst = generate_vst() 
            
            visit = PatientVisits(
            patient=patient,
            visit_type=visitType,
            vst=vst,
            primary_service=primary_service,
            insurance_name=insuranceName,
            insurance_number=insuranceNumber,
            authorization_code=verificationCode,
            visit_reason=visitReason,
            referral_number=referral_number
                          
               
            )
            visit.save()

        return JsonResponse({'status': 'success'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}) 
    

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

@csrf_exempt     
@require_POST
def add_remotepatient_visit(request):
    try:
        visit_id = request.POST.get('visit_id')
        visitType = request.POST.get('visitType')      
        patient_id = request.POST.get('patient_id')   
        primary_service = request.POST.get('primary_service')  
        
        patient = Patients.objects.get(pk=patient_id)
        if visit_id:
            # Editing existing HealthIssue item
            visit = RemotePatientVisits.objects.get(pk=visit_id)
            visit.visit_type = visitType         
            visit.patient = patient
            visit.primary_service = primary_service
    
                            
            visit.save()
        else:
            # Adding new PatientVisit item
            vst = remotegenerate_vst() 
            
            visit = RemotePatientVisits(
            patient=patient,
            visit_type=visitType,
            vst=vst,
            primary_service=primary_service,
         
                          
               
            )
            visit.save()

        return JsonResponse({'status': 'success'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}) 
    

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
 

    


   
def fetch_model_data(request):
    selected_option = request.GET.get('selected_option')
    data = []

    if selected_option == 'disease':
        data = list(DiseaseRecode.objects.values_list('id', 'disease_name'))
    elif selected_option == 'pathology':
        data = list(PathodologyRecord.objects.values_list('id', 'name'))
    elif selected_option == 'health_issue':
        data = list(HealthIssue.objects.values_list('id', 'name'))

    return JsonResponse({'data': data})    

def patient_visit_history_view(request, patient_id):
    # Retrieve visit history for the specified patient
    visit_history = PatientVisits.objects.filter(patient_id=patient_id)
    current_date = timezone.now().date()
    patient = Patients.objects.get(id=patient_id)
    medicines = Medicine.objects.filter(
        medicineinventory__remain_quantity__gt=0,  # Inventory level greater than zero
        expiration_date__gt=current_date  # Not expired
    ).distinct() 

    return render(request, 'hod_template/manage_patient_visit_history.html', {
        'visit_history': visit_history,
        'patient':patient,
        'medicines':medicines,
        })
def patient_health_record_view(request, patient_id):
    # Retrieve visit history for the specified patient
    visit_history = PatientVisits.objects.filter(patient_id=patient_id)
    patient = Patients.objects.get(id=patient_id)

    return render(request, 'hod_template/manage_patitent_health_record.html', {'visit_history': visit_history,'patient':patient})


def prescription_list(request):
    # Retrieve all prescriptions from the database
    prescriptions = Prescription.objects.all()
    patients = Patients.objects.all()
    current_date = timezone.now().date()

    # Retrieve medicines with inventory levels not equal to zero or greater than zero, and not expired
    medicines = Medicine.objects.filter(
        medicineinventory__remain_quantity__gt=0,  # Inventory level greater than zero
        expiration_date__gt=current_date  # Not expired
    ).distinct() 
    total_price = sum(prescription.total_price for prescription in prescriptions) 
    return render(request, 'hod_template/manage_prescription_list.html', {
        'prescriptions': prescriptions,
        'medicines': medicines,
        'patients': patients,
        'total_price': total_price,
        })
    
def patient_vital_list(request, patient_id):
    # Retrieve the patient object
    patient = Patients.objects.get(pk=patient_id)
    range_51 = range(51)
    range_301 = range(301)
    range_101 = range(101)
    range_15 = range(3, 16)
    # Retrieve all vital information for the patient
    patient_vitals = PatientVital.objects.filter(patient=patient).order_by('-recorded_at')

    # Render the template with the patient's vital information
    context = {
        'range_51': range_51,
        'range_301': range_301,
        'range_101': range_101,
        'range_15': range_15,
        'patient': patient, 
        'patient_vitals': patient_vitals
    }
    
    return render(request, 'hod_template/manage_patient_vital_list.html', context)    
def patient_vital_all_list(request):
    # Retrieve the patient object
    patients = Patients.objects.all()
    range_51 = range(51)
    range_301 = range(301)
    range_101 = range(101)
    range_15 = range(3, 16)
    # Retrieve all vital information for the patient
    patient_vitals = PatientVital.objects.all().order_by('-recorded_at')
    
    context = {
        'range_51': range_51,
        'range_301': range_301,
        'range_101': range_101,
        'range_15': range_15,
        'patients': patients, 
        'patient_vitals': patient_vitals
    }
    # Render the template with the patient's vital information
    return render(request, 'hod_template/manage_all_patient_vital.html', context)    

@csrf_exempt
@require_POST
def save_patient_vital(request):
    try:
        # Extract data from the request
        vital_id = request.POST.get('vital_id')
        patient_id = request.POST.get('patient_id')
        respiratory_rate = request.POST.get('respiratory_rate')
        pulse_rate = request.POST.get('pulse_rate')
        blood_pressure = request.POST.get('blood_pressure')
        spo2 = request.POST.get('spo2')
        temperature = request.POST.get('temperature')
        gcs = request.POST.get('gcs')
        avpu = request.POST.get('avpu')

        # Retrieve the corresponding InventoryItem
        patient = Patients.objects.get(id=patient_id)
       
              


        # Check if the usageHistoryId is provided for editing
        if vital_id:
            # Editing existing usage history
            vital = PatientVital.objects.get(pk=vital_id)
          
        else:
            # Creating new usage history
            vital = PatientVital()
         

        # Update or set values for other fields
        vital.respiratory_rate = respiratory_rate
        vital.pulse_rate = pulse_rate
        vital.blood_pressure = blood_pressure
        vital.spo2 = spo2
        vital.gcs = gcs
        vital.temperature = temperature
        vital.avpu = avpu
        vital.patient = patient

    
        vital.save()

        return JsonResponse({'status': 'success'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)})
    
def consultation_notes_view(request):
    consultation_notes = ConsultationNotes.objects.all()  
    pathology_records = PathodologyRecord.objects.all()# Fetch all consultation notes from the database
    patients = Patients.objects.all()# Fetch all consultation notes from the database
    doctors = Staffs.objects.filter(role='doctor')
    provisional_diagnoses = Diagnosis.objects.all()
    final_diagnoses = Diagnosis.objects.all()
    return render(request, 'hod_template/manage_consultation_notes.html', {
        'consultation_notes': consultation_notes,
        'pathology_records': pathology_records,
        'provisional_diagnoses': provisional_diagnoses,
        'final_diagnoses': final_diagnoses,
        'patients': patients,
        'doctors': doctors,
        })    


@csrf_exempt
@require_POST
def save_consultation_notes(request):
    try:
        # Extract data from the request
        notes_id = request.POST.get('notes_id')
        doctor_id = request.POST.get('doctor')
        patient_id = request.POST.get('patient')
        chief_complaints = request.POST.get('chief_complaints')
        history_of_presenting_illness = request.POST.get('history_of_presenting_illness')
        physical_examination = request.POST.get('physical_examination')
        allergy_to_medications = request.POST.get('allergy_to_medications')
        provisional_diagnosis = request.POST.getlist('provisional_diagnosis')
        final_diagnosis = request.POST.getlist('final_diagnosis')
        pathology_ids = request.POST.getlist('pathology')  # Assuming pathology is a ManyToMany field
        doctor_plan = request.POST.get('doctor_plan')

        # Retrieve the corresponding patient and doctor objects
        patient = Patients.objects.get(id=patient_id)
        doctor = Staffs.objects.get(id=doctor_id)

        # Check if the notes ID is provided for editing
        if notes_id:
            # Editing existing consultation notes
            consultation_notes = ConsultationNotes.objects.get(pk=notes_id)
        else:
            # Creating new consultation notes
            consultation_notes = ConsultationNotes()

        # Update or set values for consultation notes fields
        consultation_notes.doctor = doctor
        consultation_notes.patient = patient
        consultation_notes.chief_complaints = chief_complaints
        consultation_notes.history_of_presenting_illness = history_of_presenting_illness
        consultation_notes.physical_examination = physical_examination
        consultation_notes.allergy_to_medications = allergy_to_medications
        consultation_notes.doctor_plan = doctor_plan
        consultation_notes.save()
        
        # Update ManyToMany fields
        consultation_notes.pathology.set(pathology_ids)
        consultation_notes.provisional_diagnosis.set(provisional_diagnosis)
        consultation_notes.final_diagnosis.set(final_diagnosis)

        return JsonResponse({'status': 'success'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)})
    
def diagnosis_list(request):
    diagnoses = Diagnosis.objects.all().order_by('-created_at')    
    return render(request, 'hod_template/manage_diagnosis_list.html', {'diagnoses': diagnoses}) 


@csrf_exempt
@require_POST
def save_diagnosis(request):
    try:
        # Extract data from the request
        diagnosis_name = request.POST.get('diagnosis_name')
        diagnosis_id = request.POST.get('diagnosis_id')

        # Check if the Diagnosis ID is provided for editing
        if diagnosis_id:
            # Editing existing diagnosis
            diagnosis = Diagnosis.objects.get(pk=diagnosis_id)
            diagnosis.diagnosis_name = diagnosis_name
        else:
            # Creating a new diagnosis
            diagnosis = Diagnosis.objects.create(diagnosis_name=diagnosis_name)

        diagnosis.save()

        return JsonResponse({'status': 'success'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)})
    
    
def patient_info_form(request):
    if request.method == 'POST':
        try:
            # Retrieve data from the form submission
            first_name = request.POST.get('first_name')
            middle_name = request.POST.get('middle_name')
            last_name = request.POST.get('last_name')
            gender = request.POST.get('gender')
            occupation = request.POST.get('occupation')
            phone = request.POST.get('phone')
            employee_number = request.POST.get('employee_number')
            date_of_first_employment = request.POST.get('date_of_first_employment')
            longtime_illness = request.POST.get('longtime_illness')
            longtime_medication = request.POST.get('longtime_medication')
            osha_certificate = request.POST.get('osha_certificate')
            date_of_osha_certification = request.POST.get('date_of_osha_certification')
            insurance = request.POST.get('insurance')
            insurance_company = request.POST.get('insurance_company')
            insurance_number = request.POST.get('insurance_number')
            emergency_contact_name = request.POST.get('emergency_contact_name')
            emergency_contact_relation = request.POST.get('emergency_contact_relation')
            emergency_contact_phone = request.POST.get('emergency_contact_phone')
            emergency_contact_mobile = request.POST.get('emergency_contact_mobile')
            life_style = request.POST.get('life_style')
            age = request.POST.get('age')
            marital_status = request.POST.get('marital_status')
            nationality = request.POST.get('nationality')
            tribe = request.POST.get('tribe')
            patient_type = request.POST.get('patient_type')
            company = request.POST.get('company')
            
            if date_of_first_employment == '':
                 date_of_first_employment = None

            if date_of_osha_certification == '':
                date_of_osha_certification = None
            # Create a new RemotePatient object with the submitted data
          
            
            patient = RemotePatient(            
                first_name=first_name,
                middle_name=middle_name,
                last_name=last_name,
                gender=gender,
                occupation=occupation,
                phone=phone,
                employee_number=employee_number,
                date_of_first_employment=date_of_first_employment,
                longtime_illness=longtime_illness,
                longtime_medication=longtime_medication,
                osha_certificate=osha_certificate,
                date_of_osha_certification=date_of_osha_certification,
                insurance=insurance,
                insurance_company=insurance_company,
                insurance_number=insurance_number,
                emergency_contact_name=emergency_contact_name,
                emergency_contact_relation=emergency_contact_relation,
                emergency_contact_phone=emergency_contact_phone,
                emergency_contact_mobile=emergency_contact_mobile,
                life_style=life_style,
                age=age,
                marital_status=marital_status,
                nationality=nationality,
                tribe=tribe,
                patient_type=patient_type,
                company=company
            )

            # Save the patient object to the database
            patient.save()

            # Determine which button was clicked
            if 'save_back' in request.POST:
                # Redirect to patients list
                return redirect('patients_list')  # Replace 'patients_list' with the URL name of your patients list view
            elif 'save_add_another' in request.POST:
                # Redirect to the same form to add another patient
                messages.success(request, 'Patient  record added successfully.')
                return render(request, 'hod_template/add_remotePatients.html')
            elif 'save_continue_health' in request.POST:
                # Redirect to health information form
                return redirect(reverse('save_patient_health_condition', args=[patient.id]))  # Replace 'health_info_form' with the URL name of your health information form view
        except Exception as e:
            # Handle the exception, you can log it or render an error message
            messages.error(request, f'Error adding Patient  record : {str(e)}')
            range_100 = range(100)
            return render(request, 'hod_template/add_remotePatients.html',{'range_100':range_100})

    # If the request method is not POST, render the form template
    range_100 = range(100)
    return render(request, 'hod_template/add_remotePatients.html',{'range_100':range_100})



def patients_list(request):
    patients =RemotePatient.objects.order_by('-created_at')    
    return render(request, 'hod_template/manage_remotepatients_list.html', {'patients': patients})


def save_patient_health_condition(request, patient_id):
    try:
        # Retrieve the patient object using the patient_id from URL parameters
        patient = RemotePatient.objects.get(pk=patient_id)

        if request.method == 'POST':
            # Retrieve data from the form submission
            health_condition = request.POST.get('health_condition')
            health_condition_notes = request.POST.get('health_condition_notes')

            # Create a new PatientHealthCondition object with the submitted data
            patient_health_condition = PatientHealthCondition(
                patient=patient,
                health_condition=health_condition,
                health_condition_notes=health_condition_notes
            )

            # Save the patient health condition object to the database
            patient_health_condition.save()

            # Determine which button was clicked
            if 'save_and_return' in request.POST:
                # Redirect back to patient information
                return redirect('patient_information')  # Replace with the appropriate URL name

            elif 'save_and_continue_add_another_health_record' in request.POST:
                # Redirect to add another patient health record
                messages.success(request, 'Patient  health record added successfully.')
                return redirect(reverse('save_patient_health_condition', args=[patient_id]))  # Replace with the appropriate URL name

            elif 'save_and_continue' in request.POST:
                # Redirect to add family health information
                return redirect(reverse('save_family_medical_history', args=[patient_id]))  # Replace with the appropriate URL name

    except RemotePatient.DoesNotExist:
        # Handle the case where the patient ID is not valid
        messages.error(request, f'Patient not found: {str(e)}')
        return render(request, 'hod_template/add_patient_health_condition_form.html', {'patient': patient})

    except Exception as e:
        # Handle other exceptions
        messages.error(request, f'Error adding Patient  health record : {str(e)}')
        return render(request, 'hod_template/add_patient_health_condition_form.html', {'patient': patient})

    # If the request method is not POST or if there's an error, render an empty form
    return render(request, 'hod_template/add_patient_health_condition_form.html', {'patient': patient})



def save_family_medical_history(request, patient_id):
    try:
        # Attempt to retrieve the patient object
        patient = RemotePatient.objects.get(pk=patient_id)
    except RemotePatient.DoesNotExist:
        # If the patient does not exist, raise a 404 error
        raise Http404("Patient does not exist")

    if request.method == 'POST':
        try:
            # Retrieve form data
            condition = request.POST.get('condition')
            relationship = request.POST.get('relationship')
            comments = request.POST.get('comments')

            # Create a new FamilyMedicalHistory object with the submitted data
            family_medical_history = FamilyMedicalHistory.objects.create(
                patient=patient,
                condition=condition,
                relationship=relationship,
                comments=comments
            )

            # Determine which button was clicked
            if 'save_and_continue_add_another_family_record' in request.POST:
                # Redirect to the same form to add another family record
                messages.success(request, 'Patient family health record added successfully.')
                return redirect(reverse('save_family_medical_history', args=[patient_id]))

            elif 'save_and_return' in request.POST:
                # Redirect to the patients list
                return redirect('patients_list')

        except Exception as e:
            # Handle the exception, you can log it or render an error message
            messages.error(request, f'Error adding Patient family health record : {str(e)}')
            return render(request, 'hod_template/add_patient_family_condition_form.html', {'patient': patient})

    # If the request method is not POST, render the form template
    return render(request, 'hod_template/add_patient_family_condition_form.html', {'patient': patient})


def patient_info_form_edit(request, patient_id):    
    try:
        patient = RemotePatient.objects.get(pk=patient_id)    
    except RemotePatient.DoesNotExist:
        # Handle the case where the patient does not exist
        # For example, you can redirect to an error page or return an appropriate response
        return HttpResponse("Patient not found", status=404)
    
    if request.method == 'POST':
        try:
            # Extract data from POST request
            first_name = request.POST.get('first_name')
            middle_name = request.POST.get('middle_name')
            last_name = request.POST.get('last_name')
            gender = request.POST.get('gender')
            occupation = request.POST.get('occupation')
            phone = request.POST.get('phone')
            employee_number = request.POST.get('employee_number')
            date_of_first_employment = request.POST.get('date_of_first_employment')
            longtime_illness = request.POST.get('longtime_illness')
            longtime_medication = request.POST.get('longtime_medication')
            osha_certificate = request.POST.get('osha_certificate') == '1'
            date_of_osha_certification = request.POST.get('date_of_osha_certification')
            insurance = request.POST.get('insurance')
            insurance_company = request.POST.get('insurance_company')
            insurance_number = request.POST.get('insurance_number')
            emergency_contact_name = request.POST.get('emergency_contact_name')
            emergency_contact_relation = request.POST.get('emergency_contact_relation')
            emergency_contact_phone = request.POST.get('emergency_contact_phone')
            emergency_contact_mobile = request.POST.get('emergency_contact_mobile')
            life_style = request.POST.getlist('life_style')
            age = int(request.POST.get('age'))
            marital_status = request.POST.get('marital_status')
            nationality = request.POST.get('nationality')
            tribe = request.POST.get('tribe')
            patient_type = request.POST.get('patient_type')
            company = request.POST.get('company')

            # Convert empty strings to None for date fields
            if date_of_first_employment == '':
                date_of_first_employment = None

            if date_of_osha_certification == '':
                date_of_osha_certification = None

            # Update patient object
            patient.first_name = first_name
            patient.middle_name = middle_name
            patient.last_name = last_name
            patient.gender = gender
            patient.occupation = occupation
            patient.phone = phone
            patient.employee_number = employee_number
            patient.date_of_first_employment = date_of_first_employment
            patient.longtime_illness = longtime_illness
            patient.longtime_medication = longtime_medication
            patient.osha_certificate = osha_certificate
            patient.date_of_osha_certification = date_of_osha_certification
            patient.insurance = insurance      
            patient.emergency_contact_name = emergency_contact_name
            patient.emergency_contact_relation = emergency_contact_relation
            patient.emergency_contact_phone = emergency_contact_phone
            patient.emergency_contact_mobile = emergency_contact_mobile
            patient.life_style = life_style
            patient.age = age
            patient.marital_status = marital_status
            patient.nationality = nationality
            patient.tribe = tribe
            patient.patient_type = patient_type
            patient.company = company
            if insurance == 'Insured':
                patient.insurance_company = insurance_company
                patient.insurance_number = insurance_number
            patient.save()

            if 'save_back' in request.POST:
                # Redirect to the patients list view
                return redirect('patients_list')
            elif 'save_continue_health' in request.POST:
                # Redirect to continue editing health information
                try:
        # Save the changes made to the patient's information
                    patient.save()     
    
                    return redirect(reverse('health_info_edit', args=[patient_id]))
    
                except Exception as e:
        # Handle any errors that may occur during the save operation
                    messages.error(request, f'Error saving changes: {str(e)}')
                    range_100 = range(100)
                    return render(request, 'hod_template/edit_remotepatient.html', {'patient': patient, 'range_100': range_100})
                    

        except Exception as e:
            # Handle any other exceptions that may occur during form processing
            # For example, you can log the error and render an error page
            messages.error(request, f'Error editing Patient  record : {str(e)}')
            range_100 = range(100)
            return render(request, 'hod_template/edit_remotepatient.html', {'patient': patient, 'range_100': range_100})

    # Render the template with patient data if available
    range_100 = range(100)
    return render(request, 'hod_template/edit_remotepatient.html', {'patient': patient, 'range_100': range_100})


def health_info_edit(request, patient_id):
    try:
        patient = RemotePatient.objects.get(pk=patient_id)
        patient_health_condition =PatientHealthCondition.objects.filter(patient=patient).first()
        
        if request.method == 'POST':
            health_condition = request.POST.get('health_condition')
            health_condition_notes = request.POST.get('health_condition_notes')
            
            # Update patient's health condition
            patient_health_condition.health_condition = health_condition
            patient_health_condition.health_condition_notes = health_condition_notes
            patient_health_condition.save()
            
            if 'save_and_return' in request.POST:
                return redirect('patients_list')
            elif 'save_and_continue_family_health' in request.POST:
                return redirect('family_health_info_edit', patient_id=patient.id)

            elif 'save_and_continue_add_another_health_record' in request.POST:
                # Redirect to add another patient health record
                messages.success(request, 'Patient  health record added successfully.')
                return redirect(reverse('save_patient_health_condition', args=[patient_id])) 
        # Prepopulate form fields with existing data
        initial_data = {
            'health_condition': patient_health_condition.health_condition,
            'health_condition_notes': patient_health_condition.health_condition_notes
        }
        
        return render(request, 'hod_template/edit_patient_health_condition_form.html', {'patient': patient, 'initial_data': initial_data})
    
    except Exception as e:
        messages.error(request, f'Error editing Patient  health record : {str(e)}')
        initial_data = {
            'health_condition': patient_health_condition.health_condition,
            'health_condition_notes': patient_health_condition.health_condition_notes
        }
        
        return render(request, 'hod_template/edit_patient_health_condition_form.html', {'patient': patient, 'initial_data': initial_data})
    
def family_health_info_edit(request, patient_id):
    try:
        # Retrieve existing family medical history record for the patient
        patient = RemotePatient.objects.get(pk=patient_id)
        family_medical_history = FamilyMedicalHistory.objects.filter(patient=patient).first()
        print(family_medical_history)
        if request.method == 'POST':
            condition = request.POST.get('condition')
            relationship = request.POST.get('relationship')
            comments = request.POST.get('comments')

            # Update the existing family medical history instance
            if family_medical_history:
                family_medical_history.condition = condition
                family_medical_history.relationship = relationship
                family_medical_history.comments = comments
                family_medical_history.save()
                messages.success(request, 'Patient family health record edited successfully.')
            else:
                messages.error(request, 'Family medical history record does not exist for this patient.')

            # Check which button was clicked
            if 'save_and_continue_add_another_family_record' in request.POST:
                return redirect(reverse('family_health_info_edit', args=[patient_id]))
            elif 'save_and_return' in request.POST:
                # Redirect to the patients list page
                return redirect('patients_list')

    except Exception as e:
        messages.error(request, f'Error occurred: {e}')
        # Redirect back to the edit page with an error message
        return redirect(reverse('family_health_info_edit', args=[patient_id]))

    context = {
        'patient': patient,
        'family_medical_history': family_medical_history
    }

    return render(request, 'hod_template/edit_patient_family_condition_form.html', context)


