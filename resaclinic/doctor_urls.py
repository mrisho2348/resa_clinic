
from django.urls import include, path

from clinic import DoctorView, delete, editView, imports


urlpatterns = [
     
   
        path('doctor_dashboard/', DoctorView.doctor_dashboard, name='doctor_dashboard'),
        path('fetch_consultation_counts/', DoctorView.fetch_consultation_counts, name='fetch_consultation_counts'),
        path('unread_appointments/', DoctorView.unread_appointments_view, name='unread_appointments'),
        path('read_appointments/', DoctorView.read_appointments_view, name='read_appointments'),
        path('prescriptions/<str:visit_number>/<int:patient_id>/', DoctorView.prescription_detail, name='prescription_detail'),
        path('add_remotepatient_visit/',DoctorView.add_remotepatient_visit, name="add_remotepatient_visit"),
        path('save_consultation_notes/',DoctorView.save_consultation_notes, name="save_consultation_notes"),
        path('save_patient_vital/',DoctorView.save_patient_vital, name="save_patient_vital"),
        path('add_prescription/',DoctorView.add_prescription, name="add_prescription"),
        path('save_edited_patient/',DoctorView.save_edited_patient, name="save_edited_patient"),
        path('add_patient_visit/',DoctorView.add_patient_visit, name="add_patient_visit"),
        path('fetch_model_data/', DoctorView.fetch_model_data, name='fetch_model_data'),
        path('save_consultation_data/', DoctorView.save_consultation_data, name='save_consultation_data'),
        path('save_consultation_fee/', DoctorView.save_consultation_fee, name='save_consultation_fee'),
        path('add_pathodology_record/', DoctorView.add_pathodology_record, name='add_pathodology_record'),
        path('add_remotepatient_visit', DoctorView.add_remotepatient_visit, name='add_remotepatient_visit'),  # Move this line here
        path('add_patient/', DoctorView.add_patient, name='add_patient'),
        path('accounts/', include('django.contrib.auth.urls')), 
        path('staff_detail/<int:staff_id>/', DoctorView.single_staff_detail, name='single_staff_detail'),
        path('view-patient/<int:patient_id>/', DoctorView.view_patient, name='view_patient'),
        path('save_service_data/',DoctorView.save_service_data, name="save_service_data"),
        path('get_item_quantity/',DoctorView.get_item_quantity, name="get_item_quantity"),
        path('quality_control_list/',DoctorView.quality_control_list, name="quality_control_list"),
        path('resa/save-diagnostic-test',DoctorView.save_diagnostic_test, name="save_diagnostic_test"),    
          
        # manage urls 

        path('diagnosis/', DoctorView.diagnosis_list, name='diagnosis_list'),
        path('save_remotepatient_vital/', DoctorView.save_remotepatient_vital, name='save_remotepatient_vital'),
        path('save_remoteconsultation_notes/', DoctorView.save_remoteconsultation_notes, name='save_remoteconsultation_notes'),
        path('consultation-notes/', DoctorView.consultation_notes_view, name='consultation_notes'),
        path('resa/patient_vital_all_listt/', DoctorView.patient_vital_all_list, name='patient_vital_all_list'),    
        path('patient_consultation_detail/<int:patient_id>/', DoctorView.patient_consultation_detail, name='patient_consultation_detail'),
        path('patient_vital_list/<int:patient_id>/', DoctorView.patient_vital_list, name='patient_vital_list'),
        path('patient_health_record_view/<int:patient_id>/', DoctorView.patient_health_record_view, name='patient_health_record_view'),
        path('patient_visit_history/<int:patient_id>/', DoctorView.patient_visit_history_view, name='patient_visit_history_view'),
        path('prescriptions/', DoctorView.prescription_list, name='prescription_list'),
        path('resa/manage-referral/', DoctorView.manage_referral, name='manage_referral'),
        path('resa/patient-procedure-view/', DoctorView.patient_procedure_view, name='patient_procedure_view'),
        path('resa/all-patients',DoctorView.manage_patient, name="manage_patient"),
        path('resa/consultation-queue',DoctorView.manage_consultation, name="manage_consultation"),
        path('consultation-fees/', DoctorView.consultation_fee_list, name='consultation_fee_list'),
        path('diagnostic_tests/', DoctorView.diagnostic_tests_view, name='diagnostic_tests'),
        path('resa/manage-service',DoctorView.manage_service, name="manage_service"),
        path('resa/manage-pathodology',DoctorView.manage_pathodology, name="manage_pathodology"),
        path('resa/appointments/', DoctorView.appointment_list_view, name='appointment_list'),
        path('notifications/', DoctorView.notification_view, name='notification_view'),
        path('confirm_meeting/<int:appointment_id>/', DoctorView.confirm_meeting, name='confirm_meeting'),
        path('generate-bill/<int:procedure_id>/', DoctorView.generate_billing, name='generate_billing'),
        path('edit_meeting/<int:appointment_id>/', DoctorView.edit_meeting, name='edit_meeting'), 
        path('save_procedure/', DoctorView.save_procedure, name='save_procedure'),
        path('save_referral/', DoctorView.save_referral, name='save_referral'),  
        path('change_referral_status/', DoctorView.change_referral_status, name='change_referral_status'), 
        
        # imports urls 
        path('resa/import_Import/import_patient_vital_records',imports.import_patient_vital_records, name="import_patient_vital_records"),
        path('resa/import_Import/Inventory/ItemForm_records',imports.import_ImportInventoryItemForm_records, name="import_ImportInventoryItemForm_records"),
        path('resa/ImportExcel_service',imports.import_service_records, name="import_service_records"),
        path('import_prescription_records', imports.import_prescription_records, name='import_prescription_records'),
        path('import_consultation_notes_records', imports.import_consultation_notes_records, name='import_consultation_notes_records'),   
        path('import-patients/', imports.import_patient_records, name='import_patient_records'),
        path('import-pathology-records/', imports.import_pathology_records, name='import_pathology_records'),
        path('import-medicine-records/', imports.import_medicine_records, name='import_medicine_records'),
        path('import-procedure-records/', imports.import_procedure_records, name='import_procedure_records'),
        path('import-referral-records/', imports.import_referral_records, name='import_referral_records'),
              
        # edit urls       
        path('insurance-records/<int:insurance_id>/edit/', editView.edit_insurance, name='edit_insurance'),
        path('pathodology/<int:pathodology_id>/edit/', editView.edit_pathodology, name='edit_pathodology'),
        path('company/<int:company_id>/edit/', editView.edit_company, name='edit_company'),
        path('update_consultation_data/<int:appointment_id>/', editView.update_consultation_data, name='update_consultation_data'), 
        path('Patient/<int:patient_id>/edit/', editView.edit_patient, name='edit_patient'),
        path('update_consultation_fee/', editView.update_consultation_fee, name='update_consultation_fee'), 
        path('edit_procedure/', editView.edit_procedure, name='edit_procedure'), 
        path('edit_referral/', editView.edit_referral, name='edit_referral'), 
        path('Patient/<int:patient_id>/add/', DoctorView.appointment_view, name='appointment_view'), 
        path('appointment_view/<int:patient_id>/', DoctorView.appointment_view_remote, name='appointment_view_remote'),
        path('patient-procedure-history/<str:mrn>/view/', DoctorView.patient_procedure_history_view, name='patient_procedure_history_view_mrn'),   
        
        # delete urls 
        path('delete_diagnosis/<int:diagnosis_id>/', delete.delete_diagnosis, name='delete_diagnosis'),
        path('delete_ConsultationNotes/<int:consultation_id>/', delete.delete_ConsultationNotes, name='delete_ConsultationNotes'),
        path('delete_patient_vital/<int:vital_id>/', delete.delete_patient_vital, name='delete_patient_vital'),
        path('delete_prescription/<int:prescription_id>/', delete.delete_prescription, name='delete_prescription'),
        path('delete-consultation-fee/<int:fee_id>/', delete.delete_consultation_fee, name='delete_consultation_fee'),
        path('delete-consultation/<int:appointment_id>/', delete.delete_consultation, name='delete_consultation'),
        path('delete-diagnostic/test/<int:test_id>/', delete.delete_diagnostic_test, name='delete_diagnostic_test'),
        path('delete_patient/<int:patient_id>/', delete.delete_patient, name='delete_patient'),
        path('delete_remote_service/<int:service_id>/', delete.delete_remote_service, name='delete_remote_service'),
        path('pathodology/<int:pathodology_id>/delete/', delete.delete_pathodology, name='delete_pathodology'),
        path('company/<int:company_id>/delete/', delete.delete_company, name='delete_company'),
        path('delete_staff/<int:staff_id>/', delete.delete_staff, name='delete_staff'),
        path('delete_remote_patient/<int:patient_id>/', delete.delete_remote_patient, name='delete_remote_patient'),
        path('delete-patient/<int:patient_id>/', delete.delete_patient, name='delete_patient'),
        path('delete_service/', delete.delete_service, name='delete_service'),
        path('delete_procedure/', delete.delete_procedure, name='delete_procedure'),        
        path('delete_referral/', delete.delete_referral, name='delete_referral'),
        path('delete_patient_visit/<int:patient_visit_id>/', delete.delete_patient_visit, name='delete_patient_visit'),

   
        

        
      
        

]
