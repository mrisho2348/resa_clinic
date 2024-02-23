from django import forms

from clinic.models import Company, DiseaseRecode, InsuranceCompany, PathodologyRecord, Staffs
from .resources import DiseaseRecodeResource, InsuranceCompanyResource, StaffResources
from django.core.validators import FileExtensionValidator

class ImportStaffForm(forms.Form):
    staff_file = forms.FileField(
        label='Choose an Excel file',
        validators=[FileExtensionValidator(allowed_extensions=['xlsx', 'xls'])],
        widget=forms.ClearableFileInput(attrs={'class': 'form-control', 'accept': '.xlsx, .xls'})
    )
class ImportDiseaseForm(forms.Form):
    disease_recode_file = forms.FileField(
        label='Choose an Excel file',
        validators=[FileExtensionValidator(allowed_extensions=['xlsx', 'xls'])],
        widget=forms.ClearableFileInput(attrs={'class': 'form-control', 'accept': '.xlsx, .xls'})
    )
    
class ImportInsuranceCompanyForm(forms.Form):
    insurance_company_file = forms.FileField(
        label='Choose an Excel file',
        validators=[FileExtensionValidator(allowed_extensions=['xlsx', 'xls'])],
        widget=forms.ClearableFileInput(attrs={'class': 'form-control', 'accept': '.xlsx, .xls'})
    )
class ImportCompanyForm(forms.Form):
    company_file = forms.FileField(
        label='Choose an Excel file',
        validators=[FileExtensionValidator(allowed_extensions=['xlsx', 'xls'])],
        widget=forms.ClearableFileInput(attrs={'class': 'form-control', 'accept': '.xlsx, .xls'})
    )
class ImportPathologyRecordForm(forms.Form):
    pathology_records_file = forms.FileField(
        label='Choose an Excel file',
        validators=[FileExtensionValidator(allowed_extensions=['xlsx', 'xls'])],
        widget=forms.ClearableFileInput(attrs={'class': 'form-control', 'accept': '.xlsx, .xls'})
    )
class ImportPatientsForm(forms.Form):
    patient_records_file = forms.FileField(
        label='Choose an Excel file',
        validators=[FileExtensionValidator(allowed_extensions=['xlsx', 'xls'])],
        widget=forms.ClearableFileInput(attrs={'class': 'form-control', 'accept': '.xlsx, .xls'})
    )
    
class ImportMedicineForm(forms.Form):
    medicine_records_file = forms.FileField(
        label='Choose an Excel file',
        validators=[FileExtensionValidator(allowed_extensions=['xlsx', 'xls'])],
        widget=forms.ClearableFileInput(attrs={'class': 'form-control', 'accept': '.xlsx, .xls'})
    )
class ImportProcedureForm(forms.Form):
    procedure_records_file = forms.FileField(
        label='Choose an Excel file',
        validators=[FileExtensionValidator(allowed_extensions=['xlsx', 'xls'])],
        widget=forms.ClearableFileInput(attrs={'class': 'form-control', 'accept': '.xlsx, .xls'})
    )
class ImportReferralForm(forms.Form):
    referral_records_file = forms.FileField(
        label='Choose an Excel file',
        validators=[FileExtensionValidator(allowed_extensions=['xlsx', 'xls'])],
        widget=forms.ClearableFileInput(attrs={'class': 'form-control', 'accept': '.xlsx, .xls'})
    )
class ImportServiceForm(forms.Form):
    service_records_file = forms.FileField(
        label='Choose an Excel file',
        validators=[FileExtensionValidator(allowed_extensions=['xlsx', 'xls'])],
        widget=forms.ClearableFileInput(attrs={'class': 'form-control', 'accept': '.xlsx, .xls'})
    )
class ImportCategoryForm(forms.Form):
    category_records_file = forms.FileField(
        label='Choose an Excel file',
        validators=[FileExtensionValidator(allowed_extensions=['xlsx', 'xls'])],
        widget=forms.ClearableFileInput(attrs={'class': 'form-control', 'accept': '.xlsx, .xls'})
    )
class ImportSupplierForm(forms.Form):
    supplier_records_file = forms.FileField(
        label='Choose an Excel file',
        validators=[FileExtensionValidator(allowed_extensions=['xlsx', 'xls'])],
        widget=forms.ClearableFileInput(attrs={'class': 'form-control', 'accept': '.xlsx, .xls'})
    )
class ImportInventoryItemForm(forms.Form):
    InventoryItem_records_file = forms.FileField(
        label='Choose an Excel file',
        validators=[FileExtensionValidator(allowed_extensions=['xlsx', 'xls'])],
        widget=forms.ClearableFileInput(attrs={'class': 'form-control', 'accept': '.xlsx, .xls'})
    )
class ImportEquipmentForm(forms.Form):
    equipment_records_file = forms.FileField(
        label='Choose an Excel file',
        validators=[FileExtensionValidator(allowed_extensions=['xlsx', 'xls'])],
        widget=forms.ClearableFileInput(attrs={'class': 'form-control', 'accept': '.xlsx, .xls'})
    )
class ImportEquipmentMaintenanceForm(forms.Form):
    maintenance_records_file = forms.FileField(
        label='Choose an Excel file',
        validators=[FileExtensionValidator(allowed_extensions=['xlsx', 'xls'])],
        widget=forms.ClearableFileInput(attrs={'class': 'form-control', 'accept': '.xlsx, .xls'})
    )
class ImportReagentForm(forms.Form):
    reagent_records_file = forms.FileField(
        label='Choose an Excel file',
        validators=[FileExtensionValidator(allowed_extensions=['xlsx', 'xls'])],
        widget=forms.ClearableFileInput(attrs={'class': 'form-control', 'accept': '.xlsx, .xls'})
    )
class ImportHealthIssueForm(forms.Form):
    health_records_file = forms.FileField(
        label='Choose an Excel file',
        validators=[FileExtensionValidator(allowed_extensions=['xlsx', 'xls'])],
        widget=forms.ClearableFileInput(attrs={'class': 'form-control', 'accept': '.xlsx, .xls'})
    )
class ImportPrescriptionForm(forms.Form):
    prescription_records_file = forms.FileField(
        label='Choose an Excel file',
        validators=[FileExtensionValidator(allowed_extensions=['xlsx', 'xls'])],
        widget=forms.ClearableFileInput(attrs={'class': 'form-control', 'accept': '.xlsx, .xls'})
    )
class ImportPatientVitalForm(forms.Form):
    vital_records_file = forms.FileField(
        label='Choose an Excel file',
        validators=[FileExtensionValidator(allowed_extensions=['xlsx', 'xls'])],
        widget=forms.ClearableFileInput(attrs={'class': 'form-control', 'accept': '.xlsx, .xls'})
    )
class ImportDiagnosisForm(forms.Form):
    diagnosis_records_file = forms.FileField(
        label='Choose an Excel file',
        validators=[FileExtensionValidator(allowed_extensions=['xlsx', 'xls'])],
        widget=forms.ClearableFileInput(attrs={'class': 'form-control', 'accept': '.xlsx, .xls'})
    )
class ImportConsultationNotesForm(forms.Form):
    consultation_records_file = forms.FileField(
        label='Choose an Excel file',
        validators=[FileExtensionValidator(allowed_extensions=['xlsx', 'xls'])],
        widget=forms.ClearableFileInput(attrs={'class': 'form-control', 'accept': '.xlsx, .xls'})
    )
class ImportRemoteServiceForm(forms.Form):
    service_records_file = forms.FileField(
        label='Choose an Excel file',
        validators=[FileExtensionValidator(allowed_extensions=['xlsx', 'xls'])],
        widget=forms.ClearableFileInput(attrs={'class': 'form-control', 'accept': '.xlsx, .xls'})
    )
class ImportRemotePatientForm(forms.Form):
    patient_records_file = forms.FileField(
        label='Choose an Excel file',
        validators=[FileExtensionValidator(allowed_extensions=['xlsx', 'xls'])],
        widget=forms.ClearableFileInput(attrs={'class': 'form-control', 'accept': '.xlsx, .xls'})
    )

class StaffsForm(forms.ModelForm):
    class Meta:
        model = Staffs
        fields = '__all__'

class DiseaseRecodeForm(forms.ModelForm):
    class Meta:
        model = DiseaseRecode
        fields = '__all__'
        
class InsuranceCompanyForm(forms.ModelForm):
    class Meta:
        model = InsuranceCompany
        fields = '__all__'
        # Assign the resource to the form
        resource_class = InsuranceCompanyResource        

class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = '__all__'        
        
class PathologyRecordForm(forms.ModelForm):
    class Meta:
        model = PathodologyRecord
        fields = '__all__'        