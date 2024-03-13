
from django.urls import include, path

from clinic import  ReceptionistView, editView, imports



urlpatterns = [
        path('receptionist_dashboard/', ReceptionistView.receptionist_dashboard, name='receptionist_dashboard'),    
        path('add_patient/', ReceptionistView.add_patient, name='receptionist_add_patient'),    
        path('vehicle_ambulance_view/',ReceptionistView.vehicle_ambulance_view, name="receptionist_vehicle_ambulance_view"),
        path('vehicle_detail/<int:vehicle_id>/',ReceptionistView.vehicle_detail, name="receptionist_vehicle_detail"),
        path('ambulance_order_detail/<int:order_id>/', ReceptionistView.ambulance_order_detail, name='receptionist_ambulance_order_detail'),        
        path('get_unit_price/',ReceptionistView.get_unit_price, name="receptionist_get_unit_price"),
        path('ambulance_order_view/',ReceptionistView.ambulance_order_view, name="receptionist_ambulance_order_view"),     
        path('add_remoteprescription/',ReceptionistView.add_remoteprescription, name="receptionist_add_remoteprescription"),
        path('save_patient_vital/',ReceptionistView.save_patient_vital, name="receptionist_save_patient_vital"),
        path('add_prescription/',ReceptionistView.add_prescription, name="receptionist_add_prescription"),
        path('save_edited_patient/',ReceptionistView.save_edited_patient, name="receptionist_save_edited_patient"),
        path('add_patient_visit/',ReceptionistView.add_patient_visit, name="receptionist_add_patient_visit"),      
        path('accounts/', include('django.contrib.auth.urls')),         
        path('staff_detail/<int:staff_id>/', ReceptionistView.single_staff_detail, name='receptionist_single_staff_detail'),
        path('view-patient/<int:patient_id>/', ReceptionistView.view_patient, name='receptionist_view_patient'),  
        path('save_service_data/',ReceptionistView.save_service_data, name="receptionist_save_service_data"),      
        path('get_item_quantity/',ReceptionistView.get_item_quantity, name="receptionist_get_item_quantity"),        
        path('resa/patient_vital_all_listt/', ReceptionistView.patient_vital_all_list, name='receptionist_patient_vital_all_list'),
        path('patient_consultation_detail/<int:patient_id>/', ReceptionistView.patient_consultation_detail, name='receptionist_patient_consultation_detail'),
        path('patient_vital_list/<int:patient_id>/', ReceptionistView.patient_vital_list, name='receptionist_patient_vital_list'),
        path('patient_health_record/<int:patient_id>/<int:visit_id>/', ReceptionistView.patient_health_record, name='receptionist_patient_health_record'),
        path('patient_vital_visit_list/<int:patient_id>/<int:visit_id>/', ReceptionistView.patient_vital_visit_list, name='receptionist_patient_vital_visit_list'),
        path('patient_visit_history/<int:patient_id>/', ReceptionistView.patient_visit_history_view, name='receptionist_patient_visit_history_view'),       
        path('prescriptions/', ReceptionistView.prescription_list, name='receptionist_prescription_list'),       
        path('resa/manage-referral/', ReceptionistView.manage_referral, name='receptionist_manage_referral'),
        path('resa/patient-procedure-view/', ReceptionistView.patient_procedure_view, name='receptionist_patient_procedure_view'),      
        path('resa/all-patients',ReceptionistView.manage_patients, name="receptionist_manage_patients"),
        path('resa/consultation-queue',ReceptionistView.manage_consultation, name="receptionist_manage_consultation"),
        path('resa/manage-service',ReceptionistView.manage_service, name="receptionist_manage_service"),
        path('resa/appointments/', ReceptionistView.appointment_list_view, name='receptionist_appointment_list'),
        path('notifications/', ReceptionistView.notification_view, name='receptionist_notification_view'),
        path('generate-bill/<int:procedure_id>/', ReceptionistView.generate_billing, name='receptionist_generate_billing'),
        path('save_procedure/', ReceptionistView.save_procedure, name='receptionist_save_procedure'),
        path('save_referral/', ReceptionistView.save_referral, name='receptionist_save_referral'),
        path('change_referral_status/', ReceptionistView.change_referral_status, name='receptionist_change_referral_status'),       
        # imports urls 
        
        path('resa/ImportExcel_service',imports.import_service_records, name="receptionist_import_service_records"),     
        path('import_prescription_records', imports.import_prescription_records, name='receptionist_import_prescription_records'),
        path('import-patients/', imports.import_patient_records, name='receptionist_import_patient_records'),    
        path('import-procedure-records/', imports.import_procedure_records, name='receptionist_import_procedure_records'),
        path('import-referral-records/', imports.import_referral_records, name='receptionist_import_referral_records'), 
             
        # edit urls        
       
        path('edit-patient-disease-save/<int:patient_disease_id>/edit/', editView.edit_patient_disease_save, name='receptionist_edit_patient_disease_save'),
        path('update_consultation_data/<int:appointment_id>/', editView.update_consultation_data, name='receptionist_update_consultation_data'), 
        path('Patient/<int:patient_id>/edit/', editView.edit_patient, name='receptionist_edit_patient'),
        path('edit_procedure/', editView.edit_procedure, name='receptionist_edit_procedure'), 
        path('edit_referral/', editView.edit_referral, name='receptionist_edit_referral'), 
        path('appointment_view/', ReceptionistView.appointment_view, name='receptionist_appointment_view'), 
        path('patient-procedure-history/<str:mrn>/view/', ReceptionistView.patient_procedure_history_view, name='receptionist_patient_procedure_history_view_mrn'), 

              
]
