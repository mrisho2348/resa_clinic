from import_export import resources
from .models import Category, Company, ConsultationNotes, Diagnosis, DiseaseRecode, Equipment, EquipmentMaintenance, HealthIssue, InsuranceCompany, InventoryItem, Medicine, PathodologyRecord, PatientVital, Patients, Prescription, Procedure, Reagent, Referral, RemotePatient, RemoteService, Service, Staffs, Supplier

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
class HealthIssueResource(resources.ModelResource):
    class Meta:
        model = HealthIssue
class PrescriptionResource(resources.ModelResource):
    class Meta:
        model = Prescription
class PatientVitalResource(resources.ModelResource):
    class Meta:
        model = PatientVital
class DiagnosisResource(resources.ModelResource):
    class Meta:
        model = Diagnosis
class ConsultationNotesResource(resources.ModelResource):
    class Meta:
        model = ConsultationNotes
class RemoteServiceResource(resources.ModelResource):
    class Meta:
        model = RemoteService
class RemotePatientResource(resources.ModelResource):
    class Meta:
        model = RemotePatient