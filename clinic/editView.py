from django.shortcuts import render, redirect, get_object_or_404
from .models import Company, DiseaseRecode, InsuranceCompany, PathodologyRecord, Patients
from django.contrib import messages

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