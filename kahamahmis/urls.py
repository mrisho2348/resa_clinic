
from django.urls import include, path
from kahamahmis import KahamaReportsView, kahamaViews
from . import kahamaImports, views,delete,editView

urlpatterns = [  
        path('generate_comprehensive_report/', KahamaReportsView.generate_comprehensive_report, name='generate_comprehensive_report'),
        path('company/add/', kahamaViews.company_registration_view, name='add_clinc_company'),    # URL for editing an existing company
        path('company/edit/<int:company_id>/', kahamaViews.company_registration_view, name='edit_clinic_company'),
        path('get_formulation_unit/', kahamaViews.get_formulation_unit, name='get_formulation_unit'),
        path('get_medicine_dosage/', kahamaViews.get_medicine_dosage, name='get_medicine_dosage'),
        path('add_remote_medicine/', kahamaViews.add_remote_medicine, name='add_remote_medicine'),
        path('remotemedicine_list/', kahamaViews.remotemedicine_list, name='remotemedicine_list'),
        path('search_report/', kahamaViews.search_report, name='search_report'),
        path('patient_type_report/', kahamaViews.patient_type_report, name='patient_type_report'),
        path('pathology_record_report/', kahamaViews.pathology_record_report, name='pathology_record_report'),
        path('company_patient_report/', kahamaViews.company_patient_report, name='company_patient_report'),
        path('laboratory_report/', kahamaViews.laboratory_report, name='laboratory_report'),
        path('procedure_report/', kahamaViews.procedure_report, name='procedure_report'),
        path('referral_reports/', kahamaViews.referral_reports, name='referral_reports'),
        path('patient_statistics/', kahamaViews.patient_statistics, name='patient_statistics'),
        path('add_service/', kahamaViews.add_service, name='add_service'),
        path('delete_remote_patient/<int:patient_id>/', kahamaViews.delete_remote_patient, name='delete_remote_patient'),
        path('get_unit_price/', kahamaViews.get_unit_price, name='get_unit_price'),
        path('get_medicine_dosage/', kahamaViews.medicine_dosage, name='medicine_dosage'),
        path('appointment_view/', kahamaViews.appointment_view, name='appointment_view'), 
        path('get_drug_division_status/', kahamaViews.get_drug_division_status, name='get_drug_division_status'),
        path('verify_prescriptions/', kahamaViews.verify_prescriptions, name='verify_prescriptions'),
        path('unverify_prescriptions/', kahamaViews.unverify_prescriptions, name='unverify_prescriptions'),
        path('issue_prescriptions/', kahamaViews.issue_prescriptions, name='issue_prescriptions'),
        path('unissue_prescriptions/', kahamaViews.unissue_prescriptions, name='unissue_prescriptions'),        
        path('update_payment_status/', kahamaViews.update_payment_status, name='pay_prescriptions'),
        path('unpay_prescriptions/', kahamaViews.unpay_prescriptions, name='unpay_prescriptions'),
        path('patient_observation_history_view/<str:mrn>/view/',kahamaViews.patient_observation_history_view, name="patient_observation_history_view"),
        path('patient_lab_result_history_view/<str:mrn>/view/',kahamaViews.patient_lab_result_history_view, name="patient_lab_result_history_view"),
        path('add_remoteprescription/',kahamaViews.add_remoteprescription, name="add_remoteprescription"),
        path('patient_laboratory_view/',kahamaViews.patient_laboratory_view, name="patient_laboratory_view"),
        path('patient_observation_view/',kahamaViews.patient_observation_view, name="patient_observation_view"),
        path('get-frequency-name/', kahamaViews.get_frequency_name, name='get_frequency_name'),
        path('counsel/<int:patient_id>/<int:visit_id>/', kahamaViews.save_counsel, name='save_remote_counseling'),
        path('laboratory/<int:patient_id>/<int:visit_id>/', kahamaViews.save_laboratory, name='save_laboratory'),
        path('observation/<int:patient_id>/<int:visit_id>/', kahamaViews.save_observation, name='save_observation'),
        path('save_remoteprocedure/<int:patient_id>/<int:visit_id>/', kahamaViews.save_remoteprocedure, name='save_remoteprocedure'),
        path('save_remotereferral/<int:patient_id>/<int:visit_id>/', kahamaViews.save_remotereferral, name='save_remotereferral'),
        path('save_remote_discharges_notes/<int:patient_id>/<int:visit_id>/', kahamaViews.save_remote_discharges_notes, name='save_remote_discharges_notes'),
        path('add_primary_physical_examination/', kahamaViews.add_primary_physical_examination, name='add_primary_physical_examination'),
        path('save_chief_complaint/', kahamaViews.save_chief_complaint, name='save_chief_complaint'),
        path('delete_chief_complaint/<int:chief_complaint_id>/', kahamaViews.delete_chief_complaint, name='delete_chief_complaint'),   
         path('fetch-existing-data/', kahamaViews.fetch_existing_data, name='endpoint_to_fetch_existing_data'),       
        path('get_chief_complaints/', kahamaViews.get_chief_complaints, name='get_chief_complaints'),          
        path('delete_healthrecord/', kahamaViews.delete_healthrecord, name='delete_healthrecord'),          
        path('health_record_list',kahamaViews.health_record_list, name="health_record_list"),           
        path('save_health_record',kahamaViews.save_health_record, name="save_health_record"),           
        path('save_patient_health_information/<int:patient_id>/',kahamaViews.save_patient_health_information, name="save_patient_health_information"),
        path('get_patient_data_by_company',views.get_patient_data_by_company, name="get_patient_data_by_company"),
        path('get_gender_yearly_data',views.get_gender_yearly_data, name="get_gender_yearly_data"),
        path('get_gender_monthly_data',views.get_gender_monthly_data, name="get_gender_monthly_data"),
        
       
        path('manage_country',views.manage_country, name="manage_country"),
        path('add_remote_consultation',views.add_remote_consultation, name="add_remote_consultation"),
        path('save_remote_service',views.save_remote_service, name="save_remote_service"),
        path('edit_patient_visit_save/<int:patient_id>/',views.edit_patient_visit_save, name="edit_patient_visit_save"),
        path('edit_patient_lifestyle_behavior/<int:patient_id>/',views.edit_patient_lifestyle_behavior, name="edit_patient_lifestyle_behavior"),
        path('edit_patient_surgery_history/<int:patient_id>/',views.edit_patient_surgery_history, name="edit_patient_surgery_history"),
        path('edit_patient_medication_allergy/<int:patient_id>/',views.edit_patient_medication_allergy, name="edit_patient_medication_allergy"),
        path('save_patient_visit_save/<int:patient_id>/',views.save_patient_visit_save, name="save_patient_visit_save"),      
        path('individual_visit/<int:patient_id>/',views.individual_visit, name="individual_visit"),
        path('family_health_info_edit/<int:patient_id>/',views.family_health_info_edit, name="family_health_info_edit"),        
        path('patient_info_form_edit/<int:patient_id>/',views.patient_info_form_edit, name="patient_info_form_edit"),
        path('health_info_edit/<int:patient_id>/',views.health_info_edit, name="health_info_edit"),        
        path('patient_info_form/',views.patient_info_form, name="patient_info_form"),
        path('patient_info_form/<int:patient_id>/', views.patient_info_form, name='edit_patient'),
        path('add_remotepatient_visit/',views.add_remotepatient_visit, name="add_remotepatient_visit"),
        path('save_diagnosis/',views.save_diagnosis, name="save_diagnosis"),
        path('save_service_requests/',views.save_service_requests, name="save_service_requests"),
        path('save_consultation_notes/',views.save_consultation_notes, name="save_consultation_notes"),
        path('save_remoteconsultation_notes/',views.save_remoteconsultation_notes, name="save_remoteconsultation_notes"),
        path('save_edit_remotepatient_vitals/<int:patient_id>/',views.save_edit_remotepatient_vitals, name="save_edit_remotepatient_vitals"),
        path('save_edited_patient_visit/<int:patient_id>/',views.save_edited_patient_visit, name="save_edited_patient_visit"),
        path('save_nextremotesconsultation_notes/<int:patient_id>/<int:visit_id>/',views.save_nextremotesconsultation_notes, name="save_nextremotesconsultation_notes"),
        path('save_remotesconsultation_notes/<int:patient_id>/<int:visit_id>/',kahamaViews.save_remotesconsultation_notes, name="save_remotesconsultation_notes"),
        path('save_remotesconsultation_notes_next/<int:patient_id>/<int:visit_id>/',kahamaViews.save_remotesconsultation_notes_next, name="save_remotesconsultation_notes_next"),
        path('edit_remotesconsultation_notes/<int:patient_id>/',views.edit_remotesconsultation_notes, name="edit_remotesconsultation_notes"),
        path('save_nextprescription/<int:patient_id>/<int:visit_id>/', views.save_nextprescription, name='nextsave_prescription'),
        path('prescription/<int:patient_id>/<int:visit_id>/', views.save_prescription, name='save_prescription'),
        path('save_nextlaboratory/<int:patient_id>/<int:visit_id>/', views.save_nextlaboratory, name='nextsave_laboratory'),
        
        path('nextsave_remotereferral/<int:patient_id>/<int:visit_id>/', views.save_nextremotereferral, name='nextsave_remotereferral'),        
        path('save_nextcounsel/<int:patient_id>/<int:visit_id>/', views.save_nextcounsel, name='nextsave_counsel'),        
        path('save_nextremoteprocedure/<int:patient_id>/<int:visit_id>/', views.save_nextremoteprocedure, name='nextsave_remoteprocedure'),
        
        path('save_nextobservation/<int:patient_id>/<int:visit_id>/', views.save_nextobservation, name='nextsave_observation'),        
        path('save_patient_vital/',views.save_patient_vital, name="save_patient_vital"),
        path('save_remotepatient_vital/',views.save_remotepatient_vital, name="save_remotepatient_vital"),       
        
        path('add_patient_visit/',views.add_patient_visit, name="add_patient_visit"),
        path('add_health_issue',views.add_health_issue, name="add_health_issue"),
        path('resa/dashboard',views.kahama_dashboard, name="dashboard"),
        path('fetch_model_data/', views.fetch_model_data, name='fetch_model_data'),
        path('resa/ImportExcel',views.import_staff, name="import_staff"),      
        path('pathology_diagnostic_test_save/', views.pathology_diagnostic_test_save, name='pathology_diagnostic_test_save'),
        path('save_consultation_data/', views.save_consultation_data, name='save_consultation_data'),
        path('add_disease/', views.add_disease, name='add_disease'),
        path('save_consultation_fee/', views.save_consultation_fee, name='save_consultation_fee'),
        path('add_insurance_company/', views.add_insurance_company, name='add_insurance_company'),
        path('add_company/', views.add_company, name='add_company'),
        path('add_pathodology_record/', views.add_pathodology_record, name='add_pathodology_record'),
        path('update_equipment_status', views.update_equipment_status, name='update_equipment_status'),        
        path('kahama_login', views.ShowLoginKahama, name='kahama'),        
        path('add_remotepatient_visit', views.add_remotepatient_visit, name='add_remotepatient_visit'),  # Move this line here
        path('logout_user', views.logout_user, name='logout_user'),  # Move this line here
        path('contact/', views.ContactFormView.as_view(), name='contact_form'),
        path('GetUserDetails', views.GetUserDetails, name='GetUserDetails'),
        path('add_patient/', views.add_patient, name='add_patient'),
        path('DoLoginKahama', views.DoLoginKahama, name='DoLoginKahama'),
        path('edit_remote_company/<int:company_id>/', views.edit_remote_company, name='edit_remote_company'),
        path('save_usage_history/', views.save_usage_history, name='save_usage_history'),
        path('add_category/', views.add_category, name='add_category'),
        path('accounts/', include('django.contrib.auth.urls')),  
        path('resa/portfolio/details',views.portfolio_details, name="portfolio_details"),
        path('resa/contact',views.contact, name="contact"),
        path('resa/blog/single',views.blog_single, name="blog_single"),
        path('resa/page/404',views.page_404, name="page_404"),        
        path('resa/new-consultation',views.add_consultation, name="add_consultation"),
        path('staff_detail/<int:staff_id>/', views.single_staff_detail, name='single_staff_detail'),
        path('save_patient_visit/<int:patient_id>/', views.save_patient_visit, name='save_patient_visit'),
        path('save_nextremotepatient_vitals/<int:patient_id>/<int:visit_id>/', views.save_nextremotepatient_vitals, name='save_nextremotepatient_vitals'),
        path('save_remotepatient_vitals/<int:patient_id>/<int:visit_id>/', views.save_remotepatient_vitals, name='save_remotepatient_vitals'),
        path('view-patient/<int:patient_id>/', views.view_patient, name='view_patient'),
        path('edit_staff/<str:staff_id>', views.edit_staff, name='edit_staff'),  
        path('edit_staff_save', views.edit_staff_save, name='edit_staff_save'), 
        path('resa/new-request',views.add_request, name="add_request"),
        path('resa/update-staff-status',views.update_staff_status, name="update_staff_status"),
        path('add_inventory/',views.add_inventory, name="add_inventory"),
        path('add_supplier/', views.add_supplier, name='add_supplier'),
        path('save_sample/',views.save_sample, name="save_sample"),
        path('save_patient_disease/',views.save_patient_disease, name="save_patient_disease"),
        path('save_service_data/',views.save_service_data, name="save_service_data"),
        path('save_staff_view/',views.save_staff_view, name="save_staff_view"),
        path('get_item_quantity/',views.get_item_quantity, name="get_item_quantity"),
        path('increase_inventory_stock/',views.increase_inventory_stock, name="increase_inventory_stock"),
        path('add_inventory_item/',views.add_inventory_item, name="add_inventory_item"),
        path('get_items_below_min_stock/',views.get_items_below_min_stock, name="get_items_below_min_stock"),
        path('add_equipment/',views.add_equipment, name="add_equipment"),
        path('use_inventory_item/',views.use_inventory_item, name="use_inventory_item"),
        path('add_reagent/',views.add_reagent, name="add_reagent"),
        path('increase_reagent_stock/',views.increase_reagent_stock, name="increase_reagent_stock"),
        path('add_reagent_used/',views.add_reagent_used, name="add_reagent_used"),
        path('add_maintainance/',views.add_maintainance, name="add_maintainance"),
        path('add_quality_control/',views.add_quality_control, name="add_quality_control"),
        path('quality_control_list/',views.quality_control_list, name="quality_control_list"),
        
        
        # reports urls 
        path('resa/resa-report',views.resa_report, name="resa_report"),       
        path('resa/reports-adjustments',views.reports_adjustments, name="reports_adjustments"),
        path('resa/reports-by-visit',views.reports_by_visit, name="reports_by_visit"),
        path('resa/reports-comprehensive',views.reports_comprehensive, name="reports_comprehensive"),
        path('resa/reports-patients-visit_summary',views.reports_patients_visit_summary, name="reports_patients_visit_summary"),
        path('resa/reports-patients',views.reports_patients, name="reports_patients"),
        path('resa/reports-service',views.reports_service, name="reports_service"),
        path('resareports-stock-ledger',views.reports_stock_ledger, name="reports_stock_ledger"),
        path('resa/reports-stock-level',views.reports_stock_level, name="reports_stock_level"),
        path('resa/reports-orders',views.reports_orders, name="reports_orders"),
        path('resa/individual-visit',views.individual_visit, name="individual_visit"),
        path('resa/product-summary',views.product_summary, name="product_summary"),        
        path('get_out_of_stock_count/',views.get_out_of_stock_count, name="get_out_of_stock_count"),
        path('resa/save-diagnostic-test',views.save_diagnostic_test, name="save_diagnostic_test"),
        path('resa/in-stock-reagent-view',views.in_stock_reagent_view, name="in_stock_reagent_view"),
        path('resa/out-of-stock-reagent-view',views.out_of_stock_reagent_view, name="out_of_stock_reagent_view"),
        
       
        
        # manage urls 
        # path('resa/remotemanage_patient/', views.remotemanage_patient, name='remotemanage_patient'),
        path('patients/', views.patients_list, name='patients_list'),
        path('diagnosis/', views.diagnosis_list, name='diagnosis_list'),
        path('generatePDF/<int:patient_id>/<int:visit_id>/', views.generatePDF, name='generatePDF'),
        path('remoteservice_list/', views.remoteservice_list, name='remoteservice_list'),
        path('consultation-notes/', views.consultation_notes_view, name='consultation_notes'),
        path('resa/patient_vital_all_listt/', views.patient_vital_all_list, name='patient_vital_all_list'),
        path('resa/reagent-usage-list/', views.reagent_usage_list, name='reagent_usage_list'),
        path('resa/equipment-maintenance-list/', views.equipment_maintenance_list, name='equipment_maintenance_list'),
        path('resa/equipment-list/', views.equipment_list, name='equipment_list'),
        path('patient_vital_list/<int:patient_id>/<int:visit_id>/', views.patient_vital_list, name='patient_vital_list'),
        path('patient_visit_details_view/<int:patient_id>/<int:visit_id>/', views.patient_visit_details_view, name='patient_visit_details_view'),
        path('patient_health_record_view/<int:patient_id>/<int:visit_id>/', views.patient_health_record_view, name='patient_health_record_view'),
        path('patient_consultation_record_view/<int:patient_id>/<int:visit_id>/', views.patient_consultation_record_view, name='patient_consultation_record_view'),
        path('patient_visit_history/<int:patient_id>/', views.patient_visit_history_view, name='patient_visit_history_view'),
        path('health-issues/', views.health_issue_list, name='health_issue_list'),
        path('prescriptions/<str:visit_number>/<int:patient_id>/', views.prescription_detail, name='prescription_detail'),
        path('resa/reagent-list/', views.reagent_list, name='reagent_list'),
        path('prescriptions/', views.prescription_list, name='prescription_list'),
        path('resa/in-stock-items/', views.in_stock_items, name='in_stock_items'),
        path('resa/out-of-stock-items/', views.out_of_stock_items, name='out_of_stock_items'),
        path('resa/patient-diseases-view/', views.patient_diseases_view, name='patient_diseases_view'),
        path('pathology_diagnostic_test_list/', views.pathology_diagnostic_test_list, name='pathology_diagnostic_test_list'),
        path('resa/medication-payments-view/', views.medication_payments_view, name='medication_payments_view'),
        path('patient/medicationpayment/history/<str:mrn>/', views.patient_medicationpayment_history_view, name='patient_medicationpayment_history_view_mrn'),
        path('resa/manage-referral/', views.manage_referral, name='manage_referral'),
        path('resa/patient-procedure-view/', views.patient_procedure_view, name='patient_procedure_view'),
        path('suppliers/', views.supplier_list, name='supplier_list'),
        path('inventory/', views.inventory_list, name='inventory_list'),
        path('out_of_stock_medicines_view/', views.out_of_stock_medicines_view, name='out_of_stock_medicines_view'),
        path('usage_history/', views.usage_history_list, name='usage_history_list'),
        path('resa/medicine-inventory/', views.medicine_inventory_list, name='medicine_inventory'),
        path('resa/all-patients',views.manage_patient, name="manage_patient"),
        path('resa/consultation-queue',views.manage_consultation, name="manage_consultation"),
        path('resa/category-list/', views.category_list, name='category_list'),
        path('consultation-fees/', views.consultation_fee_list, name='consultation_fee_list'),
        path('resa/manage-company',views.manage_company, name="manage_company"),
        path('resa/manage-disease',views.manage_disease, name="manage_disease"),
        path('diagnostic_tests/', views.diagnostic_tests_view, name='diagnostic_tests'),
        path('resa/manage-staff',views.manage_staff, name="manage_staff"),
        path('resa/manage-insurance',views.manage_insurance, name="manage_insurance"),
        path('resa/manage-service',views.manage_service, name="manage_service"),
        path('resa/manage-adjustment',views.manage_adjustment, name="manage_adjustment"),
        path('resa/manage-pathodology',views.manage_pathodology, name="manage_pathodology"),
        path('resa/appointments/', views.appointment_list_view, name='appointment_list'),
        path('in_stock_medicines_view/', views.in_stock_medicines_view, name='in_stock_medicines_view'),
        path('notifications/', views.notification_view, name='notification_view'),
        path('sample_list/', views.sample_list, name='sample_list'),
        path('confirm_meeting/<int:appointment_id>/', views.confirm_meeting, name='confirm_meeting'),
        path('generate-bill/<int:procedure_id>/', views.generate_billing, name='generate_billing'),
        path('edit_meeting/<int:appointment_id>/', views.edit_meeting, name='edit_meeting'),
        path('resa/medicine-list/', views.medicine_list, name='medicine_list'),
        path('resa/medicine-expired-list/', views.medicine_expired_list, name='medicine_expired_list'),
        path('add_medicine/', views.add_medicine, name='add_medicine'),
        path('save_procedure/', views.save_procedure, name='save_procedure'),        
        path('save_referral/', views.save_referral, name='save_referral'),
        path('add_medication_payment/', views.add_medication_payment, name='add_medication_payment'),
        path('change_referral_status/', views.change_referral_status, name='change_referral_status'),
        path('api/out-of-stock-medicines/', views.out_of_stock_medicines, name='out_of_stock_medicines'),
        path('api/out-of-stock-reagent-count/', views.get_out_of_stock_count_reagent, name='get_out_of_stock_count_reagent'),
        
        # imports urls 
        path('import_medicine_drug_records', kahamaImports.import_medicine_drug_records, name='import_medicine_drug_records'),
        path('import_health_records', kahamaImports.import_health_records, name='import_health_records'),
        path('import_country_records', kahamaImports.import_country_records, name='import_country_records'),
        path('resa/import_Import/import_patient_vital_records',kahamaImports.import_patient_vital_records, name="import_patient_vital_records"),
        path('resa/import_Import/Inventory/ItemForm_records',kahamaImports.import_ImportInventoryItemForm_records, name="import_ImportInventoryItemForm_records"),
        path('resa/ImportExcel_supplier',kahamaImports.import_supplier, name="import_supplier"),
        path('resa/ImportExcel_category',kahamaImports.import_category, name="import_category"),
        path('resa/ImportExcel_service',kahamaImports.import_service_records, name="import_service_records"),
        path('resa/ImportExcel_disease',kahamaImports.import_disease_recode, name="import_disease_recode"),
        path('import-insurance-companies/', kahamaImports.import_insurance_companies, name='import_insurance_companies'),
        path('import_maintenance/', kahamaImports.import_maintenance, name='import_maintenance'),
        path('import_remoteservice_records', kahamaImports.import_remoteservice_records, name='import_remoteservice_records'),
        path('import_reagent', kahamaImports.import_reagent, name='import_reagent'),
        path('import_health_issue', kahamaImports.import_health_issue, name='import_health_issue'),
        path('import-diagnosis-records', kahamaImports.import_diagnosis_records, name='import_diagnosis_records'),
        path('import_equipment', kahamaImports.import_equipment, name='import_equipment'),
        path('import_patient', kahamaImports.import_patient, name='import_patient'),
        path('import_prescription_records', kahamaImports.import_prescription_records, name='import_prescription_records'),
        path('import_consultation_notes_records', kahamaImports.import_consultation_notes_records, name='import_consultation_notes_records'),
        path('import-companies/', kahamaImports.import_companies, name='import_companies'),
        path('import-patients/', kahamaImports.import_patient_records, name='import_patient_records'),
        path('import-pathology-records/', kahamaImports.import_pathology_records, name='import_pathology_records'),
        path('import-medicine-records/', kahamaImports.import_medicine_records, name='import_medicine_records'),
        path('import-procedure-records/', kahamaImports.import_procedure_records, name='import_procedure_records'),
        path('import-referral-records/', kahamaImports.import_referral_records, name='import_referral_records'),
        
        # edit urls 
        path('pathology-diagnostic-test-edit-save/<int:test_id>/edit/', editView.pathology_diagnostic_test_edit_save, name='pathology_diagnostic_test_edit_save'),
        path('edit-patient-disease-save/<int:patient_disease_id>/edit/', editView.edit_patient_disease_save, name='edit_patient_disease_save'),
        path('edit-sample-test/<int:sample_id>/edit/', editView.edit_sample, name='edit_sample'),
        path('diagnostic-test/<int:test_id>/edit/', editView.edit_diagnostic_test, name='edit_diagnostic_test'),
        path('disease-records/<int:disease_id>/edit/', editView.edit_disease_record, name='edit_disease_record'),
        path('insurance-records/<int:insurance_id>/edit/', editView.edit_insurance, name='edit_insurance'),
        path('pathodology/<int:pathodology_id>/edit/', editView.edit_pathodology, name='edit_pathodology'),
        path('company/<int:company_id>/edit/', editView.edit_company, name='edit_company'),
        path('update_consultation_data/<int:appointment_id>/', editView.update_consultation_data, name='update_consultation_data'), 
        path('Patient/<int:patient_id>/edit/', editView.edit_patient, name='edit_patient'),
        path('update_consultation_fee/', editView.update_consultation_fee, name='update_consultation_fee'), 
        path('edit_procedure/', editView.edit_procedure, name='edit_procedure'), 
        path('edit_lab_result/', editView.edit_lab_result, name='edit_lab_result'), 
        path('edit_observation/', editView.edit_observation, name='edit_observation'), 
        path('edit_referral/', editView.edit_referral, name='edit_referral'), 
        path('Patient/<int:patient_id>/add/', views.appointment_view, name='appointment_view'), 
        path('appointment_view/<int:patient_id>/', views.appointment_view, name='appointment_view'), 
        path('patient-procedure-history/<str:mrn>/view/', views.patient_procedure_history_view, name='patient_procedure_history_view_mrn'), 
        path('edit_medicine/<int:medicine_id>/', editView.edit_medicine, name='edit_medicine'),        
        path('edit_inventory/<int:inventory_id>/', editView.edit_inventory, name='edit_inventory'),
        
        path('edit_medication_payment/<int:payment_id>/', editView.edit_medication_payment, name='edit_medication_payment'),
        
        
        # delete urls 
        
        path('delete_diagnosis/<int:diagnosis_id>/', delete.delete_diagnosis, name='delete_diagnosis'),
        path('delete_ConsultationNotes/<int:consultation_id>/', delete.delete_ConsultationNotes, name='delete_ConsultationNotes'),
        path('delete_patient_vital/<int:vital_id>/', delete.delete_patient_vital, name='delete_patient_vital'),
        path('delete_prescription/<int:prescription_id>/', delete.delete_prescription, name='delete_prescription'),
        path('delete-consultation-fee/<int:fee_id>/', delete.delete_consultation_fee, name='delete_consultation_fee'),
        path('delete-consultation/<int:appointment_id>/', delete.delete_consultation, name='delete_consultation'),
        path('pathology-diagnostic-test-delete/<int:test_id>/', delete.pathology_diagnostic_test_delete, name='pathology_diagnostic_test_delete'),
        path('delete-patient-disease/<int:patient_disease_id>/', delete.delete_patient_disease, name='delete_patient_disease'),
        path('delete-medication-payment/<int:payment_id>/', delete.delete_medication_payment, name='delete_medication_payment'),
        path('delete-diagnostic/test/<int:test_id>/', delete.delete_diagnostic_test, name='delete_diagnostic_test'),
        path('delete_medicine/<int:medicine_id>/', delete.delete_medicine, name='delete_medicine'),
        path('disease-records/<int:disease_id>/delete/', delete.delete_disease_record, name='delete_disease_record'),
        path('delete_supplier/<int:supplier_id>/', delete.delete_supplier, name='delete_supplier'),
        path('delete_equipment/<int:equipment_id>/', delete.delete_equipment, name='delete_equipment'),
        path('delete_inventory/<int:item_id>/', delete.delete_inventory, name='delete_inventory'),
        path('delete_category/<int:category_id>/', delete.delete_category, name='delete_category'),
        path('delete_maintenance/<int:maintenance_id>/', delete.delete_maintenance, name='delete_maintenance'),
        path('delete_medicine_inventory/<int:inventory_id>/', delete.delete_medicine_inventory, name='delete_medicine_inventory'),
        path('delete_reagent/<int:reagent_id>/', delete.delete_reagent, name='delete_reagent'),
        path('delete_usage_history/<int:usage_id>/', delete.delete_usage_history, name='delete_usage_history'),
        path('delete_health_issue/<int:health_issue_id>/', delete.delete_health_issue, name='delete_health_issue'),
        path('delete_reagent_used/<int:reagentusage_id>/', delete.delete_reagent_used, name='delete_reagent_used'),
                
        path('insurance-records/<int:insurance_id>/delete/', delete.delete_insurance, name='delete_insurance'),        
        path('pathodology/<int:pathodology_id>/delete/', delete.delete_pathodology, name='delete_pathodology'),
        path('company/<int:company_id>/delete/', delete.delete_company, name='delete_company'),
        path('delete_staff/<int:staff_id>/', delete.delete_staff, name='delete_staff'),        
        path('delete-patient/<int:patient_id>/', delete.delete_patient, name='delete_patient'),
        path('delete_drug/', delete.delete_drug, name='delete_drug'),            
        path('delete_service/', delete.delete_service, name='delete_service'),            
        path('delete_procedure/', delete.delete_procedure, name='delete_procedure'),        
        path('delete_result/', delete.delete_result, name='delete_result'),        
        path('delete_observation/', delete.delete_observation, name='delete_observation'),        
        path('delete_lab_result/', delete.delete_lab_result, name='delete_lab_result'),        
        path('delete_referral/', delete.delete_referral, name='delete_referral'),
        path('delete_qualitycontrol/<int:control_id>/', delete.delete_qualitycontrol, name='delete_qualitycontrol'),
        path('delete_sample/<int:sample_id>/', delete.delete_sample, name='delete_sample'),
        
        path('delete_patient_visit/<int:patient_visit_id>/', delete.delete_patient_visit, name='delete_patient_visit'),
        path('delete_medication_payment/<int:payment_id>/', delete.delete_medication_payment, name='delete_medication_payment'),
]
