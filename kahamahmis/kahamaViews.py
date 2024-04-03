import json
from django.http import JsonResponse
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from clinic.models import Diagnosis, HealthRecord, PathodologyRecord, Service
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required

from kahamahmis.models import ChiefComplaint, FamilyMedicalHistory, PatientHealthCondition, PatientLifestyleBehavior, PatientMedicationAllergy, PatientSurgery, PrimaryPhysicalExamination, RemoteConsultationNotes, RemoteCounseling, RemoteLaboratoryOrder, RemoteObservationRecord, RemoteObservationRecord, RemotePatient, RemotePatientVisits, RemotePatientVital, RemoteProcedure, RemoteReferral, RemoteService, SecondaryPhysicalExamination
def save_patient_health_information(request, patient_id):
    try:
        # Retrieve the patient object using the patient_id from URL parameters
        patient = get_object_or_404(RemotePatient, pk=patient_id)
        if request.method == 'POST':
            # Check if the patient has allergies to medication
            medication_allergy = request.POST.get('medication_allergy')
            family_medical_history = request.POST.get('family_medical_history')
            surgery_history = request.POST.get('surgery_history')
            chronic_illness = request.POST.get('chronic_illness')
                        
            smoking = request.POST.get('smoking')
            alcohol_consumption = request.POST.get('alcohol_consumption')
            weekly_exercise_frequency = request.POST.get('weekly_exercise_frequency')
            healthy_diet = request.POST.get('healthy_diet')
            stress_management = request.POST.get('stress_management')
            sufficient_sleep = request.POST.get('sufficient_sleep')
            
            # Create PatientLifestyleBehavior object
            lifestyle_behavior = PatientLifestyleBehavior.objects.create(
                patient=patient,
                smoking=smoking,
                alcohol_consumption=alcohol_consumption,
                weekly_exercise_frequency=weekly_exercise_frequency,
                healthy_diet=healthy_diet,
                stress_management=stress_management,
                sufficient_sleep=sufficient_sleep,
            )

            # Check if the patient has surgery history
            if surgery_history == 'yes':
                surgery_names = request.POST.getlist('surgery_name[]')
                surgery_dates = request.POST.getlist('date_of_surgery[]')
                for name, date in zip(surgery_names, surgery_dates):
                    surgery = PatientSurgery.objects.create(
                        patient=patient,
                        surgery_name=name,
                        surgery_date=date,
                    )

            # Check if the patient has chronic illness
            if chronic_illness == 'yes':
                health_conditions = request.POST.getlist('health_condition[]')
                health_condition_notes = request.POST.getlist('health_condition_notes[]')
                for condition, notes in zip(health_conditions, health_condition_notes):
                    patient_health_condition = PatientHealthCondition.objects.create(
                        patient=patient,
                        health_condition=condition,
                        health_condition_notes=notes
                    )

            # Check if the patient has family medical history
            if family_medical_history == 'yes':
                conditions = request.POST.getlist('condition[]')
                relationships = request.POST.getlist('relationship[]')
                comments = request.POST.getlist('comments[]')
                for condition, relationship, comment in zip(conditions, relationships, comments):
                    family_medical_history = FamilyMedicalHistory.objects.create(
                        patient=patient,
                        condition=condition,
                        relationship=relationship,
                        comments=comment
                    )

            # Check if the patient has medication allergies
            if medication_allergy == 'yes':
                medicine_names = request.POST.getlist('medicine_name[]')
                reactions = request.POST.getlist('reaction[]')
                for medicine_name, reaction in zip(medicine_names, reactions):
                    medication_allergy = PatientMedicationAllergy.objects.create(
                        patient=patient,
                        medicine_name=medicine_name,
                        reaction=reaction
                    )

            # Redirect to the appropriate URL upon successful data saving
            return redirect(reverse('kahamahmis:save_patient_visit_save', args=[patient_id]))

    except RemotePatient.DoesNotExist:
        # Handle the case where the patient ID is not valid
        messages.error(request, 'Patient not found.')
        return redirect(reverse('kahamahmis:save_patient_health_information', args=[patient_id])) 

    except Exception as e:
        # Handle other exceptions
        messages.error(request, f'Error adding patient health information: {str(e)}')

    # If the request method is not POST or if there's an error, render the form again
    return render(request, 'kahama_template/add_patient_health_condition_form.html', {'patient': patient})


def health_record_list(request):
    records = HealthRecord.objects.all()
    return render(request, 'kahama_template/healthrecord_list.html', {'records': records})

@csrf_exempt
def save_health_record(request):
    if request.method == 'POST':
        try:
            # Extract data from POST request
            name = request.POST.get('name')
            health_record_id = request.POST.get('health_record_id')  # Check if health record ID is provided
            
            if health_record_id:  # If health record ID is provided, it's an edit operation
                # Get the existing health record object
                health_record = HealthRecord.objects.get(pk=health_record_id)
                # Update the existing health record
                health_record.name = name
                health_record.save()
            else:  # If no health record ID is provided, it's an add operation
                # Create a new health record
                HealthRecord.objects.create(name=name)
            
            # Return success response
            return JsonResponse({'success': True,'message': 'Successfully saved.'}, status=200)
        except Exception as e:
            # Return error response if an exception occurs
            return JsonResponse({'success': False, 'message': str(e)})
    else:
        # Return error response for invalid requests
        return JsonResponse({'success': False, 'message': 'Invalid request'})
    
    
@csrf_exempt      
@require_POST
def delete_healthrecord(request, health_record_id):
    try:
        health_record = get_object_or_404(HealthRecord, pk=health_record_id)
        health_record.delete()
        return JsonResponse({'status': 'success'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)})      
    
@csrf_exempt  # Use csrf_exempt decorator for simplicity in this example. For a production scenario, consider using csrf protection.
def delete_healthrecord(request):
    if request.method == 'POST':
        try:
            health_record_id = request.POST.get('health_record_id')

            # Delete procedure record
            health_record = get_object_or_404(HealthRecord, pk=health_record_id)
            health_record.delete()

            return JsonResponse({'success': True, 'message': f'health_record record for {health_record.name} deleted successfully.'})
        except HealthRecord.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Invalid health_record ID.'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': f'An error occurred: {e}'})

    return JsonResponse({'success': False, 'message': 'Invalid request method.'})
    
    
def get_chief_complaints(request):
    # Retrieve chief complaints from the HealthRecord model
    chief_complaints = HealthRecord.objects.values_list('name', flat=True)
    
    # Convert the QuerySet to a list
    chief_complaints_list = list(chief_complaints)
    
    # Return the chief complaints as JSON response
    return JsonResponse(chief_complaints_list, safe=False)    

@csrf_exempt
def save_chief_complaint(request):
    try:
        if request.method == 'POST':
            # Extract data from the request
            patient_id = request.POST.get('patient_id')
            visit_id = request.POST.get('visit_id')
            health_record_id = request.POST.get('chief_complain_name')
            other_chief_complaint = request.POST.get('other_chief_complaint')
            duration = request.POST.get('chief_complain_duration')        

            # Create a new ChiefComplaint object
            chief_complaint = ChiefComplaint(
                duration=duration,
                patient_id=patient_id,
                visit_id=visit_id
            )

            # Set the appropriate fields based on the provided data
            if health_record_id == "other":
                if ChiefComplaint.objects.filter(visit_id=visit_id,other_complaint=other_chief_complaint).exists():
                    return JsonResponse({'error': 'A ChiefComplaint with the same health record already exists for this visit'}, status=400)
                chief_complaint.other_complaint = other_chief_complaint
            else:
                # Check if a ChiefComplaint with the same health_record_id already exists for the given visit_id
                if ChiefComplaint.objects.filter(health_record_id=health_record_id, visit_id=visit_id).exists():
                    return JsonResponse({'error': 'A ChiefComplaint with the same health record already exists for this visit'}, status=400)
               
                chief_complaint.health_record_id = health_record_id          

            chief_complaint.save()

            # Initialize health_record_data to None
            health_record_data = None

            # Serialize the HealthRecord object if applicable
            if health_record_id and health_record_id != "other":
                health_record = HealthRecord.objects.get(pk=health_record_id)
                # Extract the name of the health record
                health_record_data = {'name': health_record.name}
            
            # Return the saved data as a JSON response
            response_data = {
                'id': chief_complaint.id,
                'health_record': health_record_data,
                'duration': chief_complaint.duration,
            }

            if other_chief_complaint:
                response_data['other_complaint'] = other_chief_complaint

            return JsonResponse(response_data, status=200)

        # If request method is not POST, return an error response
        return JsonResponse({'error': 'Invalid request method'}, status=400)
    except Exception as e:
        # Catch any exceptions and return an error response
        return JsonResponse({'error': str(e)}, status=500)

def fetch_existing_data(request):
    try:
        # Extract patient_id and visit_id from the request parameters
        patient_id = request.GET.get('patient_id')
        visit_id = request.GET.get('visit_id')

        # Query the database to fetch existing chief complaints based on patient_id and visit_id
        existing_data = ChiefComplaint.objects.filter(patient_id=patient_id, visit_id=visit_id).values()
        
        # Create a list to hold the modified data with unified information
        modified_data = []

        # Iterate through each entry in the existing data
        for entry in existing_data:
            # Determine the information to display based on whether the health record is null or not
            display_info = None
            if entry['health_record_id'] is not None:
                try:
                    health_record = HealthRecord.objects.get(pk=entry['health_record_id'])
                    display_info = health_record.name
                except ObjectDoesNotExist:
                    # Handle the case where the HealthRecord object does not exist
                    display_info = "Unknown Health Record"
            else:
                # Use the "other complaint" field if health record is null
                display_info = entry['other_complaint'] if entry['other_complaint'] else "Unknown"

            # Create a modified entry with unified information under the 'health_record' key
            modified_entry = {
                'id': entry['id'],
                'patient_id': entry['patient_id'],
                'visit_id': entry['visit_id'],
                'health_record': display_info,
                'duration': entry['duration'],
                'created_at': entry['created_at'],
                'updated_at': entry['updated_at']
            }

            # Add the modified entry to the list
            modified_data.append(modified_entry)

        # Return the modified data as a JSON response
        return JsonResponse(modified_data, safe=False)
    
    except Exception as e:
        # If an error occurs, return an error response with status code 500
        return JsonResponse({'error': str(e)}, status=500)
    

@csrf_exempt
def delete_chief_complaint(request, chief_complaint_id):
    try:
        # Fetch the ChiefComplaint object to delete
        chief_complaint = get_object_or_404(ChiefComplaint, id=chief_complaint_id)
        
        # Delete the ChiefComplaint
        chief_complaint.delete()
        
        # Return a success response
        return JsonResponse({'message': 'Chief complaint deleted successfully'})
    except Exception as e:
        # If an error occurs, return an error response
        return JsonResponse({'error': str(e)}, status=500)   
    
@csrf_exempt
def add_primary_physical_examination(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            primary_physical_id = data.get('primary_physical_id')  # Check if primary_physical_id is provided

            if primary_physical_id:  # If primary_physical_id is provided, update the existing record
                primary_examination = PrimaryPhysicalExamination.objects.get(id=primary_physical_id)
            else:  # Otherwise, create a new record
                # Check if a record already exists for the patient on the specified visit
                existing_record = PrimaryPhysicalExamination.objects.filter(patient_id=data.get('patient_id'), visit_id=data.get('visit_id')).first()
                if existing_record:
                    return JsonResponse({'success': False, 'error': 'A record already exists for this patient on the specified visit.'})
                
                primary_examination = PrimaryPhysicalExamination()

            # Extract data from the JSON
            primary_examination.patient_id = data.get('patient_id')
            primary_examination.visit_id = data.get('visit_id')
            primary_examination.patent_airway = data.get('airway')
            primary_examination.notpatient_explanation = data.get('explanation')
            primary_examination.breathing = data.get('breathing')
            primary_examination.normal_breathing = data.get('normalBreathing')
            primary_examination.abnormal_breathing = data.get('abnormalBreathing')
            primary_examination.circulating = data.get('circulating')
            primary_examination.normal_circulating = data.getlist('normalCirculating[]')
            primary_examination.abnormal_circulating = data.get('abnormalCirculating')
            primary_examination.gcs = data.get('gcs')
            primary_examination.rbg = data.get('rbg')
            primary_examination.pupil = data.get('pupil')
            primary_examination.pain_score = data.get('painScore')
            primary_examination.avpu = data.get('avpu')
            primary_examination.exposure = data.get('exposure')
            primary_examination.normal_exposure = data.get('temperatures')
            primary_examination.abnormal_exposure = data.get('abnormalities')

            # Save the PrimaryPhysicalExamination object
            primary_examination.save()

            # Return success response
            return JsonResponse({'success': True})

        except Exception as e:
            # Return error response
            return JsonResponse({'success': False, 'error': str(e)})

    else:
        # Return error response for unsupported request method
        return JsonResponse({'success': False, 'error': 'Unsupported request method'})
     
@login_required
def save_remotesconsultation_notes(request, patient_id, visit_id):
    doctor = request.user.staff
    patient = get_object_or_404(RemotePatient, pk=patient_id)
    visit = get_object_or_404(RemotePatientVisits, patient=patient_id, id=visit_id)
    
    try:
        health_conditions = PatientHealthCondition.objects.filter(patient_id=patient_id)
        surgery_info = PatientSurgery.objects.filter(patient_id=patient_id)
        family_history = FamilyMedicalHistory.objects.filter(patient_id=patient_id)
        allergies = PatientMedicationAllergy.objects.filter(patient_id=patient_id)
        behaviors = PatientLifestyleBehavior.objects.get(patient_id=patient_id)
        patient_vitals = RemotePatientVital.objects.filter(patient=patient_id, visit=visit)
        health_records = HealthRecord.objects.all()
        patient_surgeries = PatientSurgery.objects.filter(patient=patient_id)
    except Exception as e:
        patient_vitals = None  
        surgery_info = None  
        family_history = None  
        allergies = None  
        health_conditions = None  
        health_records = None  
        patient_surgeries = None  
        behaviors = None  
       

    consultation_note = RemoteConsultationNotes.objects.filter(patient=patient_id, visit=visit).first()
    primary_examination = PrimaryPhysicalExamination.objects.filter(patient=patient_id, visit=visit).first()
    secondary_examination = SecondaryPhysicalExamination.objects.filter(patient_id=patient_id, visit_id=visit_id).first()
    
    pathology_records = PathodologyRecord.objects.all()
    provisional_diagnoses = Diagnosis.objects.all()
    final_diagnoses = Diagnosis.objects.all()
    range_51 = range(51)
    range_301 = range(301)
    range_101 = range(101)
    range_15 = range(3, 16)
    
    context = {
        'secondary_examination': secondary_examination,
        'primary_examination': primary_examination,
        'health_records': health_records,
        'pathology_records': pathology_records,
        'provisional_diagnoses': provisional_diagnoses,
        'final_diagnoses': final_diagnoses,
        'health_conditions': health_conditions,
        'surgery_info': surgery_info,
        'family_history': family_history,
        'behaviors': behaviors,
        'allergies': allergies,
        'patient': patient,
        'visit': visit,
        'patient_vitals': patient_vitals,
        'patient_surgeries': patient_surgeries,
        'range_51': range_51,
        'range_301': range_301,
        'range_101': range_101,
        'range_15': range_15,
        'consultation_note': consultation_note,
    }

    if request.method == 'POST':
        try:
            # Retrieve form fields for consultation note      
            history_of_presenting_illness = request.POST.get('history_of_presenting_illness')
            allergy_to_medications = request.POST.get('allergy_to_medications')
            doctor_plan = request.POST.get('doctor_plan')
            provisional_diagnosis = request.POST.getlist('provisional_diagnosis[]')         
            final_diagnosis = request.POST.getlist('final_diagnosis[]')
            pathology = request.POST.getlist('pathology[]')
            
               # Retrieve form fields for secondary examination
            heent = request.POST.get('heent')
            cns = request.POST.get('cns')
            normal_cns = request.POST.get('normal_cns')
            abnormal_cns = request.POST.get('abnormal_cns')
            cvs = request.POST.get('cvs')
            normal_cvs = request.POST.get('normal_cvs')
            abnormal_cvs = request.POST.get('abnormal_cvs')
            rs = request.POST.get('rs')
            normal_rs = request.POST.get('normal_rs')
            abnormal_rs = request.POST.get('abnormal_rs')
            pa = request.POST.get('pa')
            normal_pa = request.POST.get('normal_pa')
            abnormal_pa = request.POST.get('abnormal_pa')
            gu = request.POST.get('gu')
            normal_gu = request.POST.get('normal_gu')
            abnormal_gu = request.POST.get('abnormal_gu')
            mss = request.POST.get('mss')
            normal_mss = request.POST.get('normal_mss')
            abnormal_mss = request.POST.get('abnormal_mss')

            # Retrieve form fields for primary examination
            airway = request.POST.get('airway')
            explanation = request.POST.get('explanation')
            breathing = request.POST.get('breathing')
            normal_breathing = request.POST.getlist('normalBreathing[]')
            abnormal_breathing = request.POST.get('abnormalBreathing')
            circulating = request.POST.get('circulating')
            normal_circulating = request.POST.getlist('normalCirculating[]')
            abnormal_circulating = request.POST.get('abnormalCirculating')
            gcs = request.POST.get('gcs')
            rbg = request.POST.get('rbg')
            pupil = request.POST.get('pupil')
            pain_score = request.POST.get('painScore')
            avpu = request.POST.get('avpu')
            exposure = request.POST.get('exposure')
            normal_exposure = request.POST.getlist('normal_exposure[]')
            abnormal_exposure = request.POST.get('abnormalities')

            # Handle primary examination model
            if primary_examination:                
                primary_examination.patent_airway = airway
                primary_examination.notpatient_explanation = explanation
                primary_examination.breathing = breathing
                primary_examination.normal_breathing = normal_breathing
                primary_examination.abnormal_breathing = abnormal_breathing
                primary_examination.circulating = circulating
                primary_examination.normal_circulating = normal_circulating
                primary_examination.abnormal_circulating = abnormal_circulating
                primary_examination.gcs = gcs
                primary_examination.rbg = rbg
                primary_examination.pupil = pupil
                primary_examination.pain_score = pain_score
                primary_examination.avpu = avpu
                primary_examination.exposure = exposure
                primary_examination.normal_exposure = normal_exposure
                primary_examination.abnormal_exposure = abnormal_exposure
                primary_examination.save()
            else:
                existing_record = PrimaryPhysicalExamination.objects.filter(patient_id=patient_id, visit_id=visit_id).first()
                if existing_record:
                    messages.error(request, f'A record already exists for this patient on the specified visit')
                    return render(request, 'kahama_template/add_consultation_notes.html', context)
                PrimaryPhysicalExamination.objects.create(
                    patient_id=patient_id,
                    visit_id=visit_id,
                    patent_airway = airway,
                    notpatient_explanation = explanation,
                    breathing = breathing,
                    normal_breathing = normal_breathing,
                    abnormal_breathing = abnormal_breathing,
                    circulating = circulating,
                    normal_circulating = normal_circulating,
                    abnormal_circulating = abnormal_circulating,
                    gcs = gcs,
                    rbg = rbg,
                    pupil = pupil,
                    pain_score = pain_score,
                    avpu = avpu,
                    exposure = exposure,
                    normal_exposure = normal_exposure,
                    abnormal_exposure = abnormal_exposure,
                )

            if secondary_examination:  # If record exists, update it
                secondary_examination.heent = heent
                secondary_examination.cns = cns
                secondary_examination.normal_cns = normal_cns
                secondary_examination.abnormal_cns = abnormal_cns
                secondary_examination.cvs = cvs
                secondary_examination.normal_cvs = normal_cvs
                secondary_examination.abnormal_cvs = abnormal_cvs
                secondary_examination.rs = rs
                secondary_examination.normal_rs = normal_rs
                secondary_examination.abnormal_rs = abnormal_rs
                secondary_examination.pa = pa
                secondary_examination.normal_pa = normal_pa
                secondary_examination.abnormal_pa = abnormal_pa
                secondary_examination.gu = gu
                secondary_examination.normal_gu = normal_gu
                secondary_examination.abnormal_gu = abnormal_gu
                secondary_examination.mss = mss
                secondary_examination.normal_mss = normal_mss
                secondary_examination.abnormal_mss = abnormal_mss
                secondary_examination.save()
            else:
                existing_record = SecondaryPhysicalExamination.objects.filter(patient_id=patient_id, visit_id=visit_id).first()
                if existing_record:
                    messages.error(request, f'A record already exists for this patient on the specified visit')
                    return render(request, 'kahama_template/add_consultation_notes.html', context)
                # If record doesn't exist, create a new one
                SecondaryPhysicalExamination.objects.create(
                    patient_id=patient_id,
                    visit_id=visit_id,
                    heent=heent,
                    cns=cns,
                    normal_cns=normal_cns,
                    abnormal_cns=abnormal_cns,
                    cvs=cvs,
                    normal_cvs=normal_cvs,
                    abnormal_cvs=abnormal_cvs,
                    rs=rs,
                    normal_rs=normal_rs,
                    abnormal_rs=abnormal_rs,
                    pa=pa,
                    normal_pa=normal_pa,
                    abnormal_pa=abnormal_pa,
                    gu=gu,
                    normal_gu=normal_gu,
                    abnormal_gu=abnormal_gu,
                    mss=mss,
                    normal_mss=normal_mss,
                    abnormal_mss=abnormal_mss
                )             
            

            # Handle consultation note model
            print("Provisional Diagnosis:", provisional_diagnosis)
            print("Final Diagnosis:", final_diagnosis)
            provisional_diagnosis_ids = [int(diagnosis_id) for diagnosis_id in provisional_diagnosis]
            final_diagnosis_ids = [int(diagnosis_id) for diagnosis_id in final_diagnosis]
            if consultation_note:
                consultation_note.history_of_presenting_illness = history_of_presenting_illness
                consultation_note.allergy_to_medications = allergy_to_medications
                consultation_note.doctor_plan = doctor_plan               
                consultation_note.provisional_diagnosis.set(provisional_diagnosis_ids)
                consultation_note.final_diagnosis.set(final_diagnosis_ids)
                consultation_note.pathology.set(pathology)
                try:
                    consultation_note.save()
                except Exception as e:
                    print("Error saving consultation note:", e)
            else:
                existing_record = RemoteConsultationNotes.objects.filter(patient_id=patient_id, visit_id=visit_id).first()
                if existing_record:
                    messages.error(request, f'A record already exists for this patient on the specified visit')
                    return render(request, 'kahama_template/add_consultation_notes.html', context)
                consultation_note = RemoteConsultationNotes()
                consultation_note.doctor = doctor
                consultation_note.patient = patient
                consultation_note.visit = visit
                consultation_note.history_of_presenting_illness = history_of_presenting_illness
                consultation_note.allergy_to_medications = allergy_to_medications
                consultation_note.doctor_plan = doctor_plan                
                consultation_note.provisional_diagnosis.set(provisional_diagnosis)
                consultation_note.final_diagnosis.set(final_diagnosis)
                consultation_note.pathology.set(pathology)
                consultation_note.save()

            # Redirect based on doctor's plan
            if doctor_plan == 'Prescription':
                return redirect(reverse('kahamahmis:save_prescription', args=[patient_id, visit_id]))
            elif doctor_plan == 'Laboratory':
                return redirect(reverse('kahamahmis:save_laboratory', args=[patient_id, visit_id]))
            
            elif doctor_plan == 'Referral':
                # Redirect to Referral page with necessary parameters
                return redirect(reverse('kahamahmis:save_remotereferral', args=[patient_id, visit_id]))
            elif doctor_plan == 'Counselling':
                # Redirect to Counsel page with necessary parameters
                return redirect(reverse('kahamahmis:save_remote_counseling', args=[patient_id, visit_id]))
            
            elif doctor_plan == 'Procedure':
                return redirect(reverse('kahamahmis:save_remoteprocedure', args=[patient_id, visit_id]))
            elif doctor_plan == 'Observation':
                return redirect(reverse('kahamahmis:save_observation', args=[patient_id, visit_id]))
            # Add similar logic for other plans
            
        except Exception as e:
            messages.error(request, f'Error: {str(e)}')
            # Return an appropriate response or render a template with an error message
            return render(request, 'kahama_template/add_consultation_notes.html', context)
    else:
        # If GET request, render the template for adding consultation notes
        return render(request, 'kahama_template/add_consultation_notes.html', context)
    
    
def save_counsel(request, patient_id, visit_id):
    # Retrieve patient and visit objects
    patient = get_object_or_404(RemotePatient, id=patient_id)
    visit = get_object_or_404(RemotePatientVisits, id=visit_id)              
    
    # Retrieve existing remote counseling record if it exists
    remote_counseling = RemoteCounseling.objects.filter(patient=patient, visit=visit).first()
    
    # Prepare context for rendering the template
    context = {
        'patient': patient, 
        'visit': visit,
        'remote_counseling': remote_counseling,
    }
    
    # Handle form submission
    if request.method == 'POST':
        topic = request.POST.get('topic')
        description = request.POST.get('description')             
        
        # Check if all required fields are present
        if topic and description and patient_id:
            try:
                # Update or create remote counseling record
                if remote_counseling:
                    # If the record exists, update it
                    remote_counseling.topic = topic
                    remote_counseling.description = description
                    remote_counseling.save()
                    messages.success(request, 'Remote counseling updated successfully.')
                else:
                    # If the record doesn't exist, create a new one
                    existing_record = RemoteCounseling.objects.filter(patient_id=patient_id, visit_id=visit_id).first()
                    if existing_record:
                        messages.error(request, f'A record already exists for this patient on the specified visit')
                        return render(request, 'kahama_template/counsel_template.html', context)
                    else:
                        RemoteCounseling.objects.create(
                            topic=topic,
                            description=description,
                            patient=patient,
                            visit=visit
                        )
                        messages.success(request, 'Remote counseling saved successfully.')               
             
                return redirect(reverse('kahamahmis:save_remote_counseling', args=[patient_id, visit_id]))
                
            except Exception as e:                
                messages.error(request, f'Error: {str(e)}')
        else:          
            messages.error(request, 'Please fill out all required fields.')
   
    return render(request, 'kahama_template/counsel_template.html', context)

def save_remotereferral(request, patient_id, visit_id):
      # Retrieve patient and visit objects
    patient = get_object_or_404(RemotePatient, id=patient_id)
    visit = get_object_or_404(RemotePatientVisits, id=visit_id)        
    # Check if a referral record already exists for this patient on the specified visit
    referral = RemoteReferral.objects.filter(patient=patient, visit=visit).first()   
    context = {'patient': patient, 'visit': visit, 'referral': referral}  
    try:
         
        if request.method == 'POST':
            # Process the form data if it's a POST request
            source_location = request.POST.get('source_location')
            destination_location = request.POST.get('destination_location')
            reason = request.POST.get('reason')

            if referral:
                # If a referral record exists, update it
                referral.source_location = source_location
                referral.destination_location = destination_location
                referral.reason = reason
                referral.save()
                messages.success(request, 'Remote referral updated successfully.')
            else:
                 # If the record doesn't exist, create a new one
                existing_record = RemoteReferral.objects.filter(patient_id=patient_id, visit_id=visit_id).first()
                if existing_record:
                    messages.error(request, f'A record already exists for this patient on the specified visit')
                    return render(request, 'kahama_template/save_remotereferral.html', context)
                # If no referral record exists, create a new one
                RemoteReferral.objects.create(
                    patient=patient,
                    visit=visit,
                    source_location=source_location,
                    destination_location=destination_location,
                    reason=reason
                )
                messages.success(request, 'Remote referral saved successfully.')

            # Redirect to a success page or another view
            return redirect(reverse('kahamahmis:save_remotereferral', args=[patient_id, visit_id])) # Change 'success_page' to the URL name of your success page
        
        else:          
            return render(request, 'kahama_template/save_remotereferral.html', context)    
    except Exception as e:
        messages.error(request, f'An error occurred: {str(e)}')
        return render(request, 'kahama_template/save_remotereferral.html', context)  
    
def save_remoteprocedure(request, patient_id, visit_id):
    patient = get_object_or_404(RemotePatient, id=patient_id)
    visit = get_object_or_404(RemotePatientVisits, id=visit_id)
    procedures = Service.objects.filter(type_service='Procedure')
    context = {'patient': patient, 'visit': visit,'procedures': procedures}
    existing_procedure = RemoteProcedure.objects.filter(patient_id=patient_id, visit_id=visit_id).first()

    if request.method == 'POST':
        name_id = request.POST.get('name')
        description = request.POST.get('description')
        cost = request.POST.get('cost')

        # Check if all required fields are present and valid
        if not (patient_id and visit_id and name_id and description and cost):
            messages.error(request, 'Please fill out all required fields.')
        else:
            try:
                # Check if a RemoteProcedure record already exists for this patient on the specified visit
                
                if existing_procedure:
                    # If a procedure exists, update it
                    existing_procedure.name_id = name_id
                    existing_procedure.description = description
                    existing_procedure.cost = cost
                    existing_procedure.save()
                    messages.success(request, 'Remote procedure updated successfully.')
                else:
                     # If the record doesn't exist, create a new one
                    existing_record = RemoteProcedure.objects.filter(patient_id=patient_id, visit_id=visit_id).first()
                    if existing_record:
                        messages.error(request, f'A record already exists for this patient on the specified visit')
                        return render(request, 'kahama_template/procedure_template.html', context)
                    RemoteProcedure.objects.create(
                        patient_id=patient_id,
                        visit_id=visit_id,
                        name_id=name_id,
                        description=description,
                        cost=cost
                    )
                    messages.success(request, 'Remote procedure saved successfully.')

                return redirect(reverse('kahamahmis:save_remoteprocedure', args=[patient_id, visit_id]))  # Change 'success_page' to your success page URL name
            except Exception as e:
                messages.error(request, f'Error: {str(e)}')

    context['existing_procedure'] = existing_procedure
    return render(request, 'kahama_template/procedure_template.html', context) 


def save_observation(request, patient_id, visit_id):
    patient = get_object_or_404(RemotePatient, id=patient_id)
    visit = get_object_or_404(RemotePatientVisits, id=visit_id)
    record_exists = RemoteObservationRecord.objects.filter(patient_id=patient_id, visit_id=visit_id).first()    
    services = Service.objects.filter(type_service='Imaging')
    context = {'patient': patient, 'visit': visit,'record_exists':record_exists,'services':services}

    if request.method == 'POST':        
        imaging_id = request.POST.get('imaging')
        description = request.POST.get('description')
        result = request.POST.get('result')
        cost = request.POST.get('cost')
        image = request.FILES.get('new_image')

        # Check if all required fields are filled
        if not (imaging_id and description and cost):
            messages.error(request, 'Please fill out all required fields.')
        else:
            try:                    
                if record_exists:
                    # If a record exists, update it
                    observation_record = RemoteObservationRecord.objects.get(patient_id=patient_id, visit_id=visit_id)
                    observation_record.imaging_id = imaging_id
                    observation_record.description = description
                    observation_record.result = result
                    observation_record.cost = cost
                    if image:
                        observation_record.image = image
                    observation_record.save()
                    messages.success(request, 'Remote observation record updated successfully.')
                else:
                     # If the record doesn't exist, create a new one
                    existing_record = RemoteObservationRecord.objects.filter(patient_id=patient_id, visit_id=visit_id).first()
                    if existing_record:
                        messages.error(request, f'A record already exists for this patient on the specified visit')
                        return render(request, 'kahama_template/observation_template.html', context)
                    # If no record exists, create a new one
                    RemoteObservationRecord.objects.create(
                        patient=patient,
                        visit=visit,                   
                        imaging_id=imaging_id,
                        description=description,
                        result=result,
                        cost=cost,
                        image=image
                    )
                    messages.success(request, 'Remote observation record saved successfully.')

                return redirect(reverse('kahamahmis:save_observation', args=[patient_id, visit_id]))  # Change 'success_page' to your success page URL name
            except Exception as e:
                messages.error(request, f'Error: {str(e)}')

    return render(request, 'kahama_template/observation_template.html', context)

def save_laboratory(request, patient_id, visit_id):
    patient = get_object_or_404(RemotePatient, id=patient_id)
    visit = get_object_or_404(RemotePatientVisits, id=visit_id)   
    services = Service.objects.filter(type_service='Laboratory')
    # Check if the laboratory order already exists for this patient on the specified visit
    laboratory_order = RemoteLaboratoryOrder.objects.filter(patient=patient, visit=visit).first()
    context = {'patient': patient, 'visit': visit,'laboratory_order':laboratory_order, 'services':services} 
    if request.method == 'POST':
        # Process the form data if it's a POST request
        name_id = request.POST.get('imaging')
        description = request.POST.get('description')
        result = request.POST.get('result')
        cost = request.POST.get('cost')
        lab_number = request.POST.get('lab_number')

        try:
            # If the laboratory order already exists, update it
            if laboratory_order:
                laboratory_order.name_id = name_id
                laboratory_order.description = description
                laboratory_order.result = result
                laboratory_order.cost = cost
                laboratory_order.lab_number = lab_number
                laboratory_order.save()
                messages.success(request, 'Laboratory order updated successfully.')
            else:
                existing_record = RemoteLaboratoryOrder.objects.filter(patient_id=patient_id, visit_id=visit_id).first()
                if existing_record:
                        messages.error(request, f'A record already exists for this patient on the specified visit')
                        return render(request, 'kahama_template/laboratory_template.html', context)
                # If no laboratory order exists, create a new one
                RemoteLaboratoryOrder.objects.create(
                    patient=patient,
                    visit=visit,
                    name_id=name_id,
                    description=description,
                    result=result,
                    cost=cost,
                    lab_number=lab_number
                )
                messages.success(request, 'Laboratory order saved successfully.')

            # Redirect to a success page or another view
            return redirect(reverse('kahamahmis:save_laboratory', args=[patient_id, visit_id]))  # Change 'success_page' to your success page URL name

        except Exception as e:
            messages.error(request, f'Error: {str(e)}')

    return render(request, 'kahama_template/laboratory_template.html', context)