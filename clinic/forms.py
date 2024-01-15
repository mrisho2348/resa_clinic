from django import forms

from clinic.models import Staffs
from .resources import StaffResources
from django.core.validators import FileExtensionValidator

class ImportStaffForm(forms.Form):
    staff_file = forms.FileField(
        label='Choose an Excel file',
        validators=[FileExtensionValidator(allowed_extensions=['xlsx', 'xls'])],
        widget=forms.ClearableFileInput(attrs={'class': 'form-control', 'accept': '.xlsx, .xls'})
    )

class StaffsForm(forms.ModelForm):
    class Meta:
        model = Staffs
        fields = '__all__'
