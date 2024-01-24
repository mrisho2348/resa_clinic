from import_export import resources
from .models import Company, DiseaseRecode, InsuranceCompany, Medicine, PathodologyRecord, Patients, Procedure, Staffs

class StaffResources(resources.ModelResource):
    class Meta:
        model = Staffs
class DiseaseRecodeResource(resources.ModelResource):
    class Meta:
        model = DiseaseRecode
        
class InsuranceCompanyResource(resources.ModelResource):
    class Meta:
        model = InsuranceCompany        
        
class CompanyResource(resources.ModelResource):
    class Meta:
        model = Company        

class PathologyRecordResource(resources.ModelResource):
    class Meta:
        model = PathodologyRecord        
# Create a resource for importing/exporting Patients data
# Create a resource for importing/exporting Patients data
class PatientsResource(resources.ModelResource):
    class Meta:
        model = Patients 
class MedicineResource(resources.ModelResource):
    class Meta:
        model = Medicine 
class ProcedureResource(resources.ModelResource):
    class Meta:
        model = Procedure 