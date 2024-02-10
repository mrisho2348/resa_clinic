from import_export import resources
from .models import Category, Company, DiseaseRecode, Equipment, EquipmentMaintenance, InsuranceCompany, InventoryItem, Medicine, PathodologyRecord, Patients, Procedure, Reagent, Referral, Service, Staffs, Supplier

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
class ReferralResource(resources.ModelResource):
    class Meta:
        model = Referral
class ServiceResource(resources.ModelResource):
    class Meta:
        model = Service
class CategoryResource(resources.ModelResource):
    class Meta:
        model = Category
class SupplierResource(resources.ModelResource):
    class Meta:
        model = Supplier
class InventoryItemResource(resources.ModelResource):
    class Meta:
        model = InventoryItem
class EquipmentResource(resources.ModelResource):
    class Meta:
        model = Equipment
class EquipmentMaintenanceResource(resources.ModelResource):
    class Meta:
        model = EquipmentMaintenance
class ReagentResource(resources.ModelResource):
    class Meta:
        model = Reagent