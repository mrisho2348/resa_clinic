# views.py
import logging
from django.shortcuts import redirect, render
from django.contrib import messages
from django.db import IntegrityError
from clinic.models import Company, DiseaseRecode, InsuranceCompany, Medicine, PathodologyRecord, Patients, Procedure
from .resources import CompanyResource, DiseaseRecodeResource, InsuranceCompanyResource, MedicineResource, PathologyRecordResource, PatientsResource, ProcedureResource
from .forms import ImportCompanyForm, ImportDiseaseForm, ImportInsuranceCompanyForm, ImportMedicineForm, ImportPathologyRecordForm, ImportPatientsForm, ImportProcedureForm
from tablib import Dataset
logger = logging.getLogger(__name__)
def import_disease_recode(request):
    if request.method == 'POST':
        form = ImportDiseaseForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                disease_recode_resource = DiseaseRecodeResource()
                new_disease_recodes = request.FILES['disease_recode_file']
                
                # Use tablib to load the imported data
                dataset = Dataset()
                imported_data = dataset.load(new_disease_recodes.read(), format='xlsx')  # Adjust format accordingly

                for data in imported_data:
                    disease_recode = DiseaseRecode(
                        disease_name=data[0],
                        code=data[1],
                        # Add other fields accordingly
                    )
                    disease_recode.save()

                return redirect('manage_disease') 
            except Exception as e:
                messages.error(request, f'An error occurred: {e}')
        else:
            messages.error(request, 'Form is not valid. Please check the file and try again.')
    else:
        form = ImportDiseaseForm()

    return render(request, 'hod_template/import_disease_recode.html', {'form': form})


def import_insurance_companies(request):
    if request.method == 'POST':
        form = ImportInsuranceCompanyForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                resource = InsuranceCompanyResource()
                new_companies = request.FILES['insurance_company_file']
                
                # Use tablib to load the imported data
                dataset = Dataset()
                imported_data = dataset.load(new_companies.read(), format='xlsx')  # Assuming you are using xlsx, adjust accordingly

                for data in imported_data:
                     insurance_recode = InsuranceCompany(
                        name=data[0],
                        phone=data[1],
                        short_name=data[2],
                        email=data[3],
                        address=data[4],
                        # Add other fields accordingly
                    )
                     insurance_recode.save()

                return redirect('manage_insurance') 
            except Exception as e:
                messages.error(request, f'An error occurred: {e}')

    else:
        form = ImportInsuranceCompanyForm()

    return render(request, 'hod_template/import_insurance_companies.html', {'form': form})


def import_companies(request):
    if request.method == 'POST':
        form = ImportCompanyForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                resource = CompanyResource()
                new_companies = request.FILES['company_file']
                
                # Use tablib to load the imported data
                dataset = resource.export()
                imported_data = dataset.load(new_companies.read(), format='xlsx')  # Assuming you are using xlsx, adjust accordingly

                for data in imported_data:
                      company_recode = Company(
                        name=data[0],
                        code=data[1],
                        category=data[2],
                      
                        # Add other fields accordingly
                    )
                      company_recode.save()

                return redirect('manage_company') 
            except Exception as e:
                logger.error(f"Error adding company: {str(e)}")
                messages.error(request, f'An error occurred: {e}')

    else:
        form = ImportCompanyForm()

    return render(request, 'hod_template/import_companies.html', {'form': form})


def import_pathology_records(request):
    if request.method == 'POST':
        form = ImportPathologyRecordForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                resource = PathologyRecordResource()
                new_records = request.FILES['pathology_records_file']
                
                # Use tablib to load the imported data
                dataset = resource.export()
                imported_data = dataset.load(new_records.read(), format='xlsx')  # Assuming you are using xlsx, adjust accordingly

                for data in imported_data:
                     pathodology_recode = PathodologyRecord(
                        name=data[0],
                        description=data[1],                     
                      
                        # Add other fields accordingly
                    )
                     pathodology_recode.save()

                return redirect('manage_pathodology') 
            except Exception as e:
                messages.error(request, f'An error occurred: {e}')

    else:
        form = ImportPathologyRecordForm()

    return render(request, 'hod_template/import_pathology_records.html', {'form': form})

def import_patient_records(request):
    if request.method == 'POST':
        form = ImportPatientsForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                resource = PatientsResource()
                new_records = request.FILES['patient_records_file']

                # Use tablib to load the imported data
                dataset = resource.export()
                imported_data = dataset.load(new_records.read(), format='xlsx')  # Assuming you are using xlsx, adjust accordingly
                
                for data in imported_data:
                    try:
                        patient_record = Patients.objects.create(
                            email=data[1],
                            fullname=data[0],                     
                            dob=data[2],                     
                            gender=data[3],                     
                            phone=data[4],                     
                            address=data[5],                     
                            nationality=data[6],                     
                            company=data[7],                     
                            marital_status=data[8],                     
                            patient_type=data[9],                     
                        )
                    except IntegrityError:
                        messages.warning(request, f'Duplicate entry found for {data[0]}. Skipping this record.')
                        continue

                    return redirect('manage_patient') 
            except Exception as e:
                messages.error(request, f'An error occurred: {e}')

    else:
        form = ImportPatientsForm()

    return render(request, 'hod_template/import_patients.html', {'form': form})


def import_procedure_records(request):
    if request.method == 'POST':
        form = ImportProcedureForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                resource = ProcedureResource()
                new_records = request.FILES['procedure_records_file']

                # Use tablib to load the imported data
                dataset = resource.export()
                imported_data = dataset.load(new_records.read(), format='xlsx')  # Assuming you are using xlsx, adjust accordingly
                
                for data in imported_data:
                    try:
                        procedure_record = Procedure.objects.create(
                            patient=Patients.objects.get(mrn=data[0]),
                            name=data[1],                     
                            description=data[2],                     
                            duration_time=data[3],                     
                            equipments_used=data[4],                     
                            cost=data[5],                     
                          )
                    except IntegrityError:
                        messages.warning(request, f'Duplicate entry found for {data[0]}. Skipping this record.')
                        continue

                    return redirect('patient_procedure_view') 
            except Exception as e:
                messages.error(request, f'An error occurred: {e}')

    else:
        form = ImportProcedureForm()

    return render(request, 'hod_template/import_procedure.html', {'form': form})

def import_medicine_records(request):
    if request.method == 'POST':
        form = ImportMedicineForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                resource = MedicineResource()
                new_records = request.FILES['medicine_records_file']

                # Use tablib to load the imported data
                dataset = resource.export()
                imported_data = dataset.load(new_records.read(), format='xlsx')  # Assuming you are using xlsx, adjust accordingly
                
                for data in imported_data:
                    try:
                        medicine_record = Medicine.objects.create(
                            name=data[0],
                            medicine_type=data[1],                     
                            side_effect=data[2],                     
                            dosage=data[3],                     
                            storage_condition=data[4],                     
                            manufacturer=data[5],                     
                            description=data[6],                     
                            expiration_date=data[7],                     
                            unit_price=data[8],                    
                                        
                        )
                    except IntegrityError:
                        messages.warning(request, f'Duplicate entry found for {data[0]}. Skipping this record.')
                        continue

                    return redirect('medicine_list') 
            except Exception as e:
                messages.error(request, f'An error occurred: {e}')

    else:
        form = ImportMedicineForm()

    return render(request, 'hod_template/import_medicine_records.html', {'form': form})


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