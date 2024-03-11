from datetime import  datetime
from django.utils import timezone
import logging
from django.db import IntegrityError
from django.shortcuts import get_object_or_404, redirect, render
from django.http import  HttpResponseBadRequest
from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.db.models import Sum
from clinic.models import  Consultation,  DiseaseRecode, Medicine, Notification,  PathodologyRecord, Patients, Procedure, Staffs
from django.views.decorators.http import require_POST
from django.contrib.contenttypes.models import ContentType
from django.db.models import OuterRef, Subquery
from .models import ConsultationFee, ConsultationNotes, ConsultationNotification, Country, Diagnosis, DiagnosticTest, Diagnosis,HealthIssue, InventoryItem, PatientVisits, PatientVital, Prescription, Procedure, Patients, QualityControl, Referral,  RemotePatientVisits, RemotePrescription, Service

def doctor_dashboard(request):
    total_patients = Patients.objects.count()
    recently_added_patients = Patients.objects.order_by('-created_at')[:6]
    doctors = Staffs.objects.filter(role='doctor')
    context = {
        'total_patients': total_patients,
        'recently_added_patients': recently_added_patients,
        'doctors': doctors,
        # 'gender_based_monthly_counts': gender_based_monthly_counts,
    }
    return render(request,"doctor_template/home_content.html",context)



@login_required
def manage_patient(request):
    patient_records=Patients.objects.all().order_by('-created_at') 
    range_121 = range(1, 121)
    all_country = Country.objects.all()
    doctors=Staffs.objects.filter(role='doctor')
    return render(request,"doctor_template/manage_patients.html", {
        "patient_records":patient_records,
        "range_121":range_121,
        "doctors":doctors,
        "all_country":all_country,
        })
    


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
    return render(request,"doctor_template/manage_consultation.html",context)



@login_required
def manage_service(request):
    services=Service.objects.all()
    context = {
        'services':services
    }
    return render(request,"doctor_template/manage_service.html",context)



@login_required
def manage_pathodology(request):
    pathodology_records=PathodologyRecord.objects.all() 
    disease_records=DiseaseRecode.objects.all() 
    return render(request,"doctor_template/manage_pathodology.html",{
        "pathodology_records":pathodology_records,
        "disease_records":disease_records,
        })


logger = logging.getLogger(__name__)





def single_staff_detail(request, staff_id):
    staff = get_object_or_404(Staffs, id=staff_id)
    # Fetch additional staff-related data  
    context = {
        'staff': staff,
     
    }

    return render(request, "doctor_template/staff_details.html", context)

def view_patient(request, patient_id):
    patient = get_object_or_404(Patients, id=patient_id)
    # Fetch additional staff-related data  
    context = {
        'patient': patient,
     
    }

    return render(request, "doctor_template/patients_detail.html", context)

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

        return render(request, "doctor_template/add_consultation.html", context)

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
    return render(request, 'doctor_template/manage_notification.html', context)

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
                
            elif appointment.status:
                # Perform the confirmation action (e.g., set status to selected status)
                appointment.status = selected_status
                appointment.save()

                # Add a success message
                messages.success(request, f"Meeting with {appointment.patient.mrn} confirmed.")
            else:
                messages.warning(request, f"Meeting with {appointment.patient.mrn} is already confirmed.")
        else:
            messages.warning(request, "Invalid request method for confirming meeting.")

    except IntegrityError as e:
        # Handle IntegrityError (e.g., database constraint violation)
        messages.error(request, f"Error confirming meeting: {str(e)}")

    return redirect('read_appointments')  # Adjust the URL name based on your actual URL structure

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





def patient_procedure_view(request):
    template_name = 'doctor_template/manage_procedure.html'
    
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

    return render(request, 'doctor_template/manage_patient_procedure.html', context)


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
    return render(request, 'doctor_template/manage_referral.html', {'referrals': referrals,'patients':patients})


def generate_billing(request, procedure_id):
    procedure = get_object_or_404(Procedure, id=procedure_id)

    context = {
        'procedure': procedure,
    }

    return render(request, 'doctor_template/billing_template.html', context)

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
    return render(request, 'doctor_template/manage_appointment.html', context)


@login_required
def fetch_consultation_counts(request):
    # Get the currently logged-in doctor staff
    doctor = request.user.staff  # Assuming user has a profile linked with Staffs model

    # Get the counts of unread and read consultations for the current doctor
    unread_count = ConsultationNotification.objects.filter(doctor=doctor, is_read=False).count()
    read_count = ConsultationNotification.objects.filter(doctor=doctor, is_read=True).count()

    # Return the counts as JSON response
    return JsonResponse({'unreadCount': unread_count, 'readCount': read_count})

def unread_appointments_view(request):
    doctor = request.user.staff
    # Fetching all unread consultations associated with the doctor
    unread_notifications = ConsultationNotification.objects.filter(doctor=doctor, is_read=False)
    unread_appointments = [notification.consultation for notification in unread_notifications]
    
    # Update the notifications as read once the user opens them
    for notification in unread_notifications:
        notification.is_read = True
        notification.save()
    
    return render(request, 'doctor_template/unread_appointments.html', {'appointments': unread_appointments})

def read_appointments_view(request):
    doctor = request.user.staff
    # Fetching all read consultations associated with the doctor
    read_notifications = ConsultationNotification.objects.filter(doctor=doctor, is_read=True)
    read_appointments = [notification.consultation for notification in read_notifications]
    
    return render(request, 'doctor_template/read_appointments.html', {'appointments': read_appointments})

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
def save_edited_patient(request):
    if request.method == 'POST':
        try:
            # Extract the form data
            patient_id = request.POST.get('patient_id')
            edited_patient = Patients.objects.get(id=patient_id)
            edited_patient.first_name = request.POST.get('edit_first_name')
            edited_patient.middle_name = request.POST.get('edit_middle_name')
            edited_patient.last_name = request.POST.get('edit_last_name')
            edited_patient.gender = request.POST.get('edit_gender')
            if not request.POST.get('edit_age'):
                edited_patient.age = None
            else:
                edited_patient.age = int(request.POST.get('edit_age'))
            
            if not request.POST.get('edit_dob'):
                edited_patient.dob = None
            else:
                edited_patient.dob = request.POST.get('edit_dob')               
            edited_patient.phone = request.POST.get('edit_phone')
            edited_patient.address = request.POST.get('edit_Address')
            edited_patient.nationality_id = request.POST.get('edit_nationality')
            edited_patient.payment_form = request.POST.get('edit_payment_type')
            if request.POST.get('edit_payment_type') == 'insurance':
                edited_patient.insurance_name = request.POST.get('insurance_name')
                edited_patient.insurance_number = request.POST.get('edit_insurance_number')           
            
            edited_patient.emergency_contact_name = request.POST.get('edit_emergency_contact_name')
            edited_patient.emergency_contact_relation = request.POST.get('edit_emergency_contact_relation')
            edited_patient.emergency_contact_phone = request.POST.get('edit_emergency_contact_phone')
            edited_patient.marital_status = request.POST.get('marital_status')
            edited_patient.patient_type = request.POST.get('edit_patient_type')

            # Save the edited patient
            edited_patient.save()

            # Return JSON response for success
            return JsonResponse({'message': 'Patient data updated successfully.'})
        except Exception as e:
            # Return JSON response for error
            return JsonResponse({'error': str(e)}, status=400)
    else:
        return JsonResponse({'error': 'Invalid request method.'}, status=400)
    
@csrf_exempt
def add_patient(request):
    try:
        if request.method == 'POST':
            # Extract data from the request
            first_name = request.POST.get('first_name')
            middle_name = request.POST.get('middle_name')
            last_name = request.POST.get('last_name')
            emergency_contact_name = request.POST.get('emergency_contact_name')
            emergency_contact_relation = request.POST.get('emergency_contact_relation')         
            emergency_contact_phone = request.POST.get('emergency_contact_phone')
            nationality_id = request.POST.get('nationality')            
            dob = request.POST.get('dob')
            gender = request.POST.get('gender')
            phone = request.POST.get('phone')
            address = request.POST.get('Address')                       
            marital_status = request.POST.get('maritalStatus')
            patient_type = request.POST.get('patient_type')
            payment_type = request.POST.get('payment_type')
            insurance_name = request.POST.get('insurance_name')
            insurance_number = request.POST.get('insurance_number')
            age = request.POST.get('age')
            if not dob:
                dob = None
            if not age:
                age = None

            # Generate the medical record number (mrn)
            mrn = generate_mrn()

            # Create an instance of the Patient model
            patient_instance = Patients(
                mrn=mrn,
                first_name=first_name,
                middle_name=middle_name,
                last_name=last_name,             
                dob=dob,
                age=age,
                gender=gender,
                phone=phone,
                address=address,
                emergency_contact_name=emergency_contact_name,
                emergency_contact_relation=emergency_contact_relation,                
                emergency_contact_phone=emergency_contact_phone,
                nationality_id=nationality_id,                
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
    new_mrn = f"RES-{new_mrn_number:07d}"

    return new_mrn
      
      


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

    return render(request, 'doctor_template/manage_diagnostic_tests.html', context)


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

    return render(request, 'doctor_template/manage_consultation_fee_list.html', {
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
    

    
    
def patient_consultation_detail(request, patient_id):
    try:        
        
        prescriptions = Prescription.objects.filter(patient=patient_id)
        try:
            consultation_notes = ConsultationNotes.objects.filter(patient_id=patient_id).order_by('-created_at').first()
        except ConsultationNotes.DoesNotExist:
            consultation_notes = None
        try:
            vital = PatientVital.objects.filter(patient=patient_id)
        except PatientVital.DoesNotExist:
            vital = None
        try:
            visit_history = PatientVisits.objects.filter(patient_id=patient_id)
        
        except:
            visit_history = None        
        pathology_records = PathodologyRecord.objects.all()  # Fetch all consultation notes from the database
        doctors = Staffs.objects.filter(role='doctor')
        provisional_diagnoses = Diagnosis.objects.all()
        final_diagnoses = Diagnosis.objects.all()

        total_price = sum(prescription.total_price for prescription in prescriptions)
        range_31 = range(31)
        current_date = timezone.now().date()
        patient = Patients.objects.get(id=patient_id)
        remote_service = Service.objects.all()
        range_51 = range(51)
        range_301 = range(301)
        range_101 = range(101)
        range_15 = range(3, 16)
        medicines = Medicine.objects.filter(
            medicineinventory__remain_quantity__gt=0,  # Inventory level greater than zero
            expiration_date__gt=current_date  # Not expired
        ).distinct()

        return render(request, 'doctor_template/patient_consultation_detail.html', {        
            'patient': patient,           
            'range_31': range_31,
            'medicines': medicines,
            'prescriptions': prescriptions,
            'total_price': total_price,
            'visit_history': visit_history,
            'consultation_notes': consultation_notes,
            'pathology_records': pathology_records,
            'doctors': doctors,
            'provisional_diagnoses': provisional_diagnoses,
            'final_diagnoses': final_diagnoses,
            'vital': vital,
            'remote_service': remote_service,
            'range_51': range_51,
            'range_301': range_301,
            'range_101': range_101,
            'range_15': range_15,
        })
    except Exception as e:
        # Handle other exceptions if necessary
        return render(request, '404.html', {'error_message': str(e)})    
    
@csrf_exempt
@require_POST
def save_remoteconsultation_notes(request):
    try:
        # Extract data from the request
        notes_id = request.POST.get('notes_id')       
        patient_id = request.POST.get('patient_id')   
        print(patient_id)     
        chief_complaints = request.POST.get('chief_complaints')
        print(chief_complaints)
        history_of_presenting_illness = request.POST.get('history_of_presenting_illness')
        physical_examination = request.POST.get('physical_examination')
        allergy_to_medications = request.POST.get('allergy_to_medications')
        provisional_diagnosis = request.POST.getlist('provisional_diagnosis')
        final_diagnosis = request.POST.getlist('final_diagnosis')
        pathology_ids = request.POST.getlist('pathology')  # Assuming pathology is a ManyToMany field
        doctor_plan = request.POST.get('doctor_plan')
        doctor = request.user.staff 
        # Retrieve the corresponding patient and doctor objects
        patient = Patients.objects.get(id=patient_id)       
        

        # Check if the notes ID is provided for editing
        if notes_id:
            # Editing existing consultation notes
            consultation_notes = ConsultationNotes.objects.get(pk=notes_id)
        else:
            # Creating new consultation notes
            consultation_notes = ConsultationNotes()

        # Update or set values for consultation notes fields
        
        consultation_notes.patient = patient        
        consultation_notes.doctor = doctor        
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
    

@csrf_exempt
@require_POST
def save_remotepatient_vital(request):
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
    return render(request, 'doctor_template/manage_quality_control_list.html', 
                  {
                      'quality_controls': quality_controls,
                      'technicians': technicians,
                      }
                  ) 


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

    return render(request, 'doctor_template/manage_patient_visit_history.html', {
        'visit_history': visit_history,
        'patient':patient,
        'medicines':medicines,
        })
def patient_health_record_view(request, patient_id):
    # Retrieve visit history for the specified patient
    visit_history = PatientVisits.objects.filter(patient_id=patient_id)
    patient = Patients.objects.get(id=patient_id)

    return render(request, 'doctor_template/manage_patitent_health_record.html', {'visit_history': visit_history,'patient':patient})


def prescription_list(request):
    # Retrieve all patients
    patients = Patients.objects.all()

    # Retrieve current date
    current_date = timezone.now().date()
    
    # Retrieve all prescriptions with related patient and visit
    prescriptions = Prescription.objects.select_related('patient', 'visit')

    # Group prescriptions by visit and calculate total price for each visit
    visit_total_prices = prescriptions.values('visit__vst', 'visit__patient__first_name','visit__created_at', 'visit__patient__id', 'visit__patient__middle_name', 'visit__patient__last_name').annotate(total_price=Sum('total_price'))
    print(visit_total_prices)
    # Retrieve medicines with inventory levels not equal to zero or greater than zero, and not expired
    medicines = Medicine.objects.filter(
        medicineinventory__remain_quantity__gt=0,  # Inventory level greater than zero
        expiration_date__gt=current_date  # Not expired
    ).distinct() 
    
    # Calculate total price of all prescriptions
    total_price = sum(prescription.total_price for prescription in prescriptions) 
    
    return render(request, 'doctor_template/manage_prescription_list.html', { 
        'medicines': medicines,
        'patients': patients,
        'total_price': total_price,
        'visit_total_prices': visit_total_prices,
    })
    
@login_required
def prescription_detail(request, visit_number, patient_id):
    patient = Patients.objects.get(id=patient_id)
    prescriptions = Prescription.objects.filter(visit__vst=visit_number, visit__patient__id=patient_id)
    context = {'patient': patient, 'prescriptions': prescriptions}
    return render(request, "doctor_template/prescription_detail.html", context)

  
    
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
    
    return render(request, 'doctor_template/manage_patient_vital_list.html', context)    
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
    return render(request, 'doctor_template/manage_all_patient_vital.html', context)    

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
    
    doctors = Staffs.objects.filter(role='doctor')
    provisional_diagnoses = Diagnosis.objects.all()
    final_diagnoses = Diagnosis.objects.all()
    patient_records=Patients.objects.all().order_by('-created_at') 
    range_121 = range(1, 121)
    all_country = Country.objects.all()
    doctors=Staffs.objects.filter(role='doctor')
    return render(request, 'doctor_template/manage_consultation_notes.html', {
        'consultation_notes': consultation_notes,
        'pathology_records': pathology_records,
        'provisional_diagnoses': provisional_diagnoses,
        'final_diagnoses': final_diagnoses,
        'patient_records': patient_records,
        'doctors': doctors,
        'range_121': range_121,
        'all_country': all_country,
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
    return render(request, 'doctor_template/manage_diagnosis_list.html', {'diagnoses': diagnoses}) 



    













