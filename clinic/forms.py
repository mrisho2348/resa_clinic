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