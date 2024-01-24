from datetime import datetime
import logging
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from .models import Company, DiseaseRecode, InsuranceCompany, PathodologyRecord, Patients, Medicine, Procedure
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.db import transaction
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required

# Define a logger
logger = logging.getLogger(__name__)
def edit_insurance(request, insurance_id):
    insurance = get_object_or_404(InsuranceCompany, pk=insurance_id)

    if request.method == 'POST':
        try:
            # Retrieve data from the form
            name = request.POST.get('Name')
            phone = request.POST.get('Phone')
            short_name = request.POST.get('Short_name')
            email = request.POST.get('Email')
            address = request.POST.get('Address')

            # Update the InsuranceCompany object
            insurance.name = name
            insurance.phone = phone
            insurance.short_name = short_name
            insurance.email = email
            insurance.address = address

            # Save the changes
            insurance.save()

            messages.success(request, 'Insurance details updated successfully!')
            return redirect('manage_insurance')  # Replace 'your_redirect_url' with the appropriate URL name

        except Exception as e:
            messages.error(request, f'An error occurred: {e}')

    return render(request, 'update/edit_insurance.html', {'insurance': insurance})


@csrf_exempt  # Use csrf_exempt decorator for simplicity in this example. For a production scenario, consider using csrf protection.
def edit_procedure(request):
    if request.method == 'POST':
        try:
            procedure_id = request.POST.get('procedure_id')
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

            # Update procedure record
            procedure_record = Procedure.objects.get(id=procedure_id)
            procedure_record.name = name          
            procedure_record.description = description
            procedure_record.equipments_used = equipments_used
            procedure_record.cost = cost
            procedure_record.duration_time = duration
            procedure_record.save()

            return JsonResponse({'success': True, 'message': f'Procedure record for {procedure_record.name} updated successfully.'})
        except Procedure.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Invalid procedure ID.'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': f'An error occurred: {e}'})

    return JsonResponse({'success': False, 'message': 'Invalid request method.'})


def edit_patient(request, patient_id):
    patient = get_object_or_404(Patients, pk=patient_id)

    if request.method == 'POST':
        try:
            # Retrieve data from the form
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

            # Update the InsuranceCompany object
            patient.fullname = fullname
            patient.phone = phone
            patient.dob = dob
            patient.email = email
            patient.address = address
            patient.gender = gender
            patient.nationality = nationality
            patient.company = company
            patient.marital_status = marital_status
            patient.patient_type = patient_type

            # Save the changes
            patient.save()

            messages.success(request, 'patient details updated successfully!')
            return redirect('manage_patient')  # Replace 'your_redirect_url' with the appropriate URL name

        except Exception as e:
            messages.error(request, f'An error occurred: {e}')

    return render(request, 'update/edit_patient.html', {'patient': patient})



def edit_medicine(request, medicine_id):
    try:
        # Check if the request method is POST
        if request.method != 'POST':
            return JsonResponse({'message': 'Invalid request method'}, status=400)

        # Get the medicine instance to be edited
        medicine = get_object_or_404(Medicine, id=medicine_id)

        # Extract the data from the request
        name = request.POST.get('name')
        medicine_type = request.POST.get('medicine_type')
        side_effect = request.POST.get('side_effect')
        dosage = request.POST.get('dosage')
        storage_condition = request.POST.get('storage_condition')
        manufacturer = request.POST.get('manufacturer')
        description = request.POST.get('description')
        expiration_date = request.POST.get('expiration_date')
        unit_price = request.POST.get('unit_price')

        # Perform the update within a transaction
        with transaction.atomic():
            # Update the medicine instance
            medicine.name = name
            medicine.medicine_type = medicine_type
            medicine.side_effect = side_effect
            medicine.dosage = dosage
            medicine.storage_condition = storage_condition
            medicine.manufacturer = manufacturer
            medicine.description = description
            medicine.expiration_date = expiration_date
            medicine.unit_price = unit_price

            # Save the changes
            medicine.save()

        # Log a success message
        messages.success(request, 'Medicine details updated successfully!')
        return redirect('medicine_list') 
    except Exception as e:
        # Log an error message
        logger.error(f'Error updating medicine details. Medicine ID: {medicine_id}, Error: {str(e)}')
        # Handle exceptions and return an error response
        return JsonResponse({'message': 'Error updating medicine details', 'error': str(e)}, status=500)
    

def edit_disease_record(request, disease_id):
    disease = get_object_or_404(DiseaseRecode, pk=disease_id)

    if request.method == 'POST':
        try:
            # Retrieve data from the form
            name = request.POST.get('Name')
            code = request.POST.get('code')

            # Update the DiseaseRecode object
            disease.disease_name = name
            disease.code = code

            # Save the changes
            disease.save()

            messages.success(request, 'Disease details updated successfully!')
            return redirect('manage_disease')  # Replace 'your_redirect_url' with the appropriate URL name

        except Exception as e:
            messages.error(request, f'An error occurred: {e}')

    return render(request, 'update/edit_disease.html', {'disease': disease})

def edit_company(request, company_id):
    company = get_object_or_404(Company, pk=company_id)

    if request.method == 'POST':
        try:
            # Retrieve data from the form
            name = request.POST.get('Name')
            code = request.POST.get('code')
            category = request.POST.get('category')

            # Update the Company object
            company.name = name
            company.code = code
            company.category = category

            # Save the changes
            company.save()

            messages.success(request, 'Company details updated successfully!')
            return redirect('manage_company')  # Replace 'your_redirect_url' with the appropriate URL name
        except Exception as e:
            messages.error(request, f'An error occurred: {e}')

    return render(request, 'update/edit_company.html', {'company': company})

def edit_pathodology(request, pathodology_id):
    pathodology = get_object_or_404(PathodologyRecord, pk=pathodology_id)

    if request.method == 'POST':
        try:
            # Retrieve data from the form
            name = request.POST.get('Name')
            description = request.POST.get('description')

            # Update the PathodologyRecord object
            pathodology.name = name
            pathodology.description = description

            # Save the changes
            pathodology.save()

            messages.success(request, 'Pathodology details updated successfully!')
            return redirect('manage_pathodology')  # Replace 'your_redirect_url' with the appropriate URL name

        except Exception as e:
            messages.error(request, f'An error occurred: {e}')

    return render(request, 'update/edit_pathodology.html', {'pathodology': pathodology})