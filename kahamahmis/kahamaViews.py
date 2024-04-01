from django.http import JsonResponse
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from clinic.models import ChiefComplaint, HealthRecord, RemotePatient, PatientLifestyleBehavior, PatientSurgery, PatientHealthCondition, FamilyMedicalHistory, PatientMedicationAllergy
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.core.exceptions import ObjectDoesNotExist
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