from datetime import date, datetime
import json
from django.utils import timezone
import logging
from django.db import models
from django.db import IntegrityError
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth import logout,login
from django.http import HttpResponse, HttpResponseBadRequest,HttpResponseRedirect
from django.template import loader
from django.shortcuts import render
from django.urls import reverse
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
from .models import DiagnosticTest, HealthIssue, MedicationPayment, Procedure, Patients, Referral, Sample

# Create your views here.
def index(request):
    return render(request,"index.html")

def dashboard(request):
    total_patients = Patients.objects.count()
    recently_added_patients = Patients.objects.order_by('-created_at')[:6]
    context = {
        'total_patients': total_patients,
        'recently_added_patients': recently_added_patients,
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

@login_required
def manage_consultation(request):
    return render(request,"hod_template/manage_consultation.html")

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
    return render(request,"hod_template/manage_service.html")

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
    return render(request,"hod_template/manage_pathodology.html",{"pathodology_records":pathodology_records})


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
        return redirect('appointment_view', patient_id=patient_id)
    
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
    # Pass the context variables to the template
    context = {
        'medicine_inventories': medicine_inventories,
        'low_quantity_medicines': low_quantity_medicines,
        'non_expired_medicines': non_expired_medicines,
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
    context = {'appointments': appointments, 'unread_notification_count': unread_notification_count}
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

            # Save data to the model
            PathodologyRecord.objects.create(
                name=name,
                description=description
            )

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
            company = request.POST.get('company')
            marital_status = request.POST.get('maritalStatus')
            patient_type = request.POST.get('patient_type')

            # Generate the medical record number (mrn)
            # You can use your own logic to generate a unique mrn
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
                company=company,
                marital_status=marital_status,
                patient_type=patient_type
            )

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
            quantity = int(request.POST.get('quantity'))
            amount = request.POST.get('amount')
            payment_date = request.POST.get('payment_date')

            # Retrieve patient and medicine instances
            patient = Patients.objects.get(mrn=patient_mrn) if patient_mrn else None
            medicine = Medicine.objects.get(id=medicine_id)

            # Create MedicationPayment instance
            medication_payment = MedicationPayment(
                patient=patient,
                non_registered_patient_name=non_registered_patient_name,
                non_registered_patient_email=non_registered_patient_email,
                non_registered_patient_phone=non_registered_patient_phone,
                medicine=medicine,
                quantity=quantity,
                amount=amount,
                payment_date=payment_date,
            )
            medication_payment.save()          

            return JsonResponse({'success': True, 'message': f'MedicationPayment record for {medication_payment} saved successfully.'})
        except Patients.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Invalid patient ID.'})
        except IntegrityError:
            return JsonResponse({'success': False, 'message': 'Duplicate entry. Referral record not saved.'})
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
        quantity__gt=100,
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
                pathology_id = request.POST.get('pathology_id')
                
            if disease_or_pathology == 'disease':
                diseases_ids = request.POST.getlist('diseases[]')                
            if disease_or_pathology == 'health_issue':
                health_issues_ids = request.POST.getlist('health_issues')
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

