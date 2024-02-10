# views.py
import logging
from django.shortcuts import redirect, render
from django.contrib import messages
from django.db import IntegrityError
from clinic.models import Category, Company, DiseaseRecode, Equipment, EquipmentMaintenance, InsuranceCompany, InventoryItem, Medicine, PathodologyRecord, Patients, Procedure, Reagent, Referral, Service, Supplier
from .resources import CategoryResource, CompanyResource, DiseaseRecodeResource, EquipmentMaintenanceResource, EquipmentResource, InsuranceCompanyResource, InventoryItemResource, MedicineResource, PathologyRecordResource, PatientsResource, ProcedureResource, ReagentResource, ReferralResource, ServiceResource, SupplierResource
from .forms import ImportCategoryForm, ImportCompanyForm, ImportDiseaseForm, ImportEquipmentForm, ImportEquipmentMaintenanceForm, ImportInsuranceCompanyForm, ImportInventoryItemForm, ImportMedicineForm, ImportPathologyRecordForm, ImportPatientsForm, ImportProcedureForm, ImportReagentForm, ImportReferralForm, ImportServiceForm, ImportSupplierForm
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

def import_category(request):
    if request.method == 'POST':
        form = ImportCategoryForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                resource = CategoryResource()
                new_category = request.FILES['category_records_file']
                
                # Use tablib to load the imported data
                dataset = Dataset()
                imported_data = dataset.load(new_category.read(), format='xlsx')  # Assuming you are using xlsx, adjust accordingly

                for data in imported_data:
                     category_recode = Category(
                        name=data[0],
                      
                    )
                     category_recode.save()

                return redirect('category_list') 
            except Exception as e:
                messages.error(request, f'An error occurred: {e}')

    else:
        form = ImportCategoryForm()

    return render(request, 'hod_template/import_category.html', {'form': form})


def import_supplier(request):
    if request.method == 'POST':
        form = ImportSupplierForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                resource = SupplierResource()
                new_supplier = request.FILES['supplier_records_file']
                
                # Use tablib to load the imported data
                dataset = Dataset()
                imported_data = dataset.load(new_supplier.read(), format='xlsx')  # Assuming you are using xlsx, adjust accordingly

                for data in imported_data:
                     supplier_record = Supplier(
                        name=data[0],
                        address=data[1],
                        contact_information=data[2],
                        email=data[3],
                      
                    )
                     supplier_record.save()

                return redirect('supplier_list') 
            except Exception as e:
                messages.error(request, f'An error occurred: {e}')

    else:
        form = ImportSupplierForm()

    return render(request, 'hod_template/import_supplier.html', {'form': form})

def import_equipment(request):
    if request.method == 'POST':
        form = ImportEquipmentForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                resource = EquipmentResource()
                new_equipment = request.FILES['equipment_records_file']
                
                # Use tablib to load the imported data
                dataset = Dataset()
                imported_data = dataset.load(new_equipment.read(), format='xlsx')  # Assuming you are using xlsx, adjust accordingly

                for data in imported_data:
                     equipment_record = Equipment(
                        name=data[0],
                        description=data[1],
                        manufacturer=data[2],
                        serial_number=data[3],
                        acquisition_date=data[4],
                        warranty_expiry_date=data[5],
                        location=data[6],
                      
                    )
                     equipment_record.save()

                return redirect('equipment_list') 
            except Exception as e:
                messages.error(request, f'An error occurred: {e}')

    else:
        form = ImportEquipmentForm()

    return render(request, 'hod_template/import_equipment.html', {'form': form})

def import_maintenance(request):
    if request.method == 'POST':
        form = ImportEquipmentMaintenanceForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                resource = EquipmentMaintenanceResource()
                new_maintenance = request.FILES['maintenance_records_file']
                
                # Use tablib to load the imported data
                dataset = Dataset()
                imported_data = dataset.load(new_maintenance.read(), format='xlsx')  # Assuming you are using xlsx, adjust accordingly

                for data in imported_data:
                     maintenance_record = EquipmentMaintenance(
                        equipment= Equipment.objects.get(id=data[0]),
                        maintenance_date=data[1],
                        technician=data[2],
                        description=data[3],
                        cost=data[4],
                        notes=data[5],
                  
                      
                    )
                     maintenance_record.save()

                return redirect('equipment_maintenance_list') 
            except Exception as e:
                messages.error(request, f'An error occurred: {e}')

    else:
        form = ImportEquipmentMaintenanceForm()

    return render(request, 'hod_template/import_maintenance.html', {'form': form})


def import_reagent(request):
    if request.method == 'POST':
        form = ImportReagentForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                resource = ReagentResource()
                new_reagent = request.FILES['reagent_records_file']
                
                # Use tablib to load the imported data
                dataset = Dataset()
                imported_data = dataset.load(new_reagent.read(), format='xlsx')  # Assuming you are using xlsx, adjust accordingly

                for data in imported_data:
                     reagent_record = Reagent(
                        name=data[0],
                        expiration_date=data[1],
                        manufacturer=data[2],
                        lot_number=data[3],
                        storage_conditions=data[4],
                        quantity_in_stock=data[5],
                        price_per_unit=data[6],
                        remaining_quantity=data[5],
                       
                  
                      
                    )
                     reagent_record.save()

                return redirect('reagent_list') 
            except Exception as e:
                messages.error(request, f'An error occurred: {e}')

    else:
        form = ImportReagentForm()

    return render(request, 'hod_template/import_reagent.html', {'form': form})


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


def import_ImportInventoryItemForm_records(request):
    if request.method == 'POST':
        form = ImportInventoryItemForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                resource = InventoryItemResource()
                new_records = request.FILES['InventoryItem_records_file']
                
                # Use tablib to load the imported data
                dataset = resource.export()
                imported_data = dataset.load(new_records.read(), format='xlsx')  # Assuming you are using xlsx, adjust accordingly

                for data in imported_data:
                     pathodology_recode = InventoryItem(
                        name=data[0],
                        quantity=data[1],                     
                        category=Category.objects.get(id=data[2]),                    
                        description=data[3],                     
                        supplier=Supplier.objects.get(id=data[4]),                     
                        purchase_date=data[5],                     
                        purchase_price=data[6],                     
                        expiry_date=data[7],                     
                        location_in_storage=data[8],                     
                        min_stock_level=data[9],                     
                        condition=data[10],                     
                        remain_quantity=data[1],                     
                      
                        # Add other fields accordingly
                    )
                     pathodology_recode.save()

                return redirect('inventory_list') 
            except Exception as e:
                messages.error(request, f'An error occurred: {e}')

    else:
        form = ImportInventoryItemForm()

    return render(request, 'hod_template/import_InventoryItem.html', {'form': form})

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


def import_service_records(request):
    if request.method == 'POST':
        form = ImportServiceForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                resource = ServiceResource()
                new_records = request.FILES['service_records_file']

                # Use tablib to load the imported data
                dataset = resource.export()
                imported_data = dataset.load(new_records.read(), format='xlsx')  # Assuming you are using xlsx, adjust accordingly
                
                for data in imported_data:
                    try:
                        service_record = Service.objects.create(
                            department=data[1],
                            type_service=data[0],                     
                            name=data[2],                     
                            description=data[3],                     
                            cost=data[4],                     
                                              
                        )
                    except IntegrityError:
                        messages.warning(request, f'Duplicate entry found for {data[0]}. Skipping this record.')
                        continue

                return redirect('manage_service') 
            except Exception as e:
                messages.error(request, f'An error occurred: {e}')

    else:
        form = ImportServiceForm()

    return render(request, 'hod_template/import_service.html', {'form': form})


def import_referral_records(request):
    if request.method == 'POST':
        form = ImportReferralForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                resource = ReferralResource()
                new_records = request.FILES['referral_records_file']

                # Use tablib to load the imported data
                dataset = resource.export()
                imported_data = dataset.load(new_records.read(), format='xlsx')  # Assuming you are using xlsx, adjust accordingly
                
                for data in imported_data:
                    try:
                        referral_record =Referral.objects.create(
                            patient=Patients.objects.get(mrn=data[0]),
                            source_location=data[1],                     
                            destination_location=data[2],                     
                            reason=data[3],                     
                            notes=data[4],                     
                                           
                        )
                    except IntegrityError:
                        messages.warning(request, f'Duplicate entry found for {data[0]}. Skipping this record.')
                        continue

                return redirect('manage_referral') 
            except Exception as e:
                messages.error(request, f'An error occurred: {e}')

    else:
        form = ImportReferralForm()

    return render(request, 'hod_template/import_referral.html', {'form': form})


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