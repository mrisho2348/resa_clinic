from import_export import resources
from .models import Company, DiseaseRecode, InsuranceCompany, PathodologyRecord, Staffs

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