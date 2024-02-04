
from django.urls import include, path

from . import views,delete,imports,editView

urlpatterns = [
        path('',views.index, name="home"),
        path('resa/dashboard',views.dashboard, name="dashboard"),
        path('resa/ImportExcel',views.import_staff, name="import_staff"),      
        path('pathology_diagnostic_test_save/', views.pathology_diagnostic_test_save, name='pathology_diagnostic_test_save'),
        path('add_disease/', views.add_disease, name='add_disease'),
        path('add_insurance_company/', views.add_insurance_company, name='add_insurance_company'),
        path('add_company/', views.add_company, name='add_company'),
        path('add_pathodology_record/', views.add_pathodology_record, name='add_pathodology_record'),
        path('login', views.ShowLogin, name='login'),        
        path('logout_user', views.logout_user, name='logout_user'),  # Move this line here
        path('contact/', views.ContactFormView.as_view(), name='contact_form'),
        path('GetUserDetails', views.GetUserDetails, name='GetUserDetails'),
        path('add_patient/', views.add_patient, name='add_patient'),
        path('dologin', views.DoLogin, name='DoLogin'),
        path('accounts/', include('django.contrib.auth.urls')),  
        path('resa/portfolio/details',views.portfolio_details, name="portfolio_details"),
        path('resa/contact',views.contact, name="contact"),
        path('resa/blog/single',views.blog_single, name="blog_single"),
        path('resa/page/404',views.page_404, name="page_404"),        
        path('resa/new-consultation',views.add_consultation, name="add_consultation"),
        path('staff_detail/<int:staff_id>/', views.single_staff_detail, name='single_staff_detail'),
        path('view-patient/<int:patient_id>/', views.view_patient, name='view_patient'),
        path('edit_staff/<str:staff_id>', views.edit_staff, name='edit_staff'),  
        path('edit_staff_save', views.edit_staff_save, name='edit_staff_save'), 
        path('resa/new-request',views.add_request, name="add_request"),
        path('resa/update-staff-status',views.update_staff_status, name="update_staff_status"),
        path('add_inventory/',views.add_inventory, name="add_inventory"),
        path('save_sample/',views.save_sample, name="save_sample"),
        path('save_patient_disease/',views.save_patient_disease, name="save_patient_disease"),
        path('save_staff_view/',views.save_staff_view, name="save_staff_view"),
        
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
        path('resa/save-diagnostic_test',views.save_diagnostic_test, name="save_diagnostic_test"),
        
       
        
        # manage urls 
        path('resa/patient-diseases-view/', views.patient_diseases_view, name='patient_diseases_view'),
        path('pathology_diagnostic_test_list/', views.pathology_diagnostic_test_list, name='pathology_diagnostic_test_list'),
        path('resa/medication-payments-view/', views.medication_payments_view, name='medication_payments_view'),
        path('patient/medicationpayment/history/<str:mrn>/', views.patient_medicationpayment_history_view, name='patient_medicationpayment_history_view_mrn'),
        path('resa/manage-referral/', views.manage_referral, name='manage_referral'),
        path('resa/patient-procedure-view/', views.patient_procedure_view, name='patient_procedure_view'),
        path('resa/medicine-inventory/', views.medicine_inventory_list, name='medicine_inventory'),
        path('resa/all-patients',views.manage_patient, name="manage_patient"),
        path('resa/consultation-queue',views.manage_consultation, name="manage_consultation"),
        path('resa/manage-company',views.manage_company, name="manage_company"),
        path('resa/manage-disease',views.manage_disease, name="manage_disease"),
        path('diagnostic_tests/', views.diagnostic_tests_view, name='diagnostic_tests'),
        path('resa/manage-staff',views.manage_staff, name="manage_staff"),
        path('resa/manage-insurance',views.manage_insurance, name="manage_insurance"),
        path('resa/manage-service',views.manage_service, name="manage_service"),
        path('resa/manage-adjustment',views.manage_adjustment, name="manage_adjustment"),
        path('resa/manage-pathodology',views.manage_pathodology, name="manage_pathodology"),
        path('resa/appointments/', views.appointment_list_view, name='appointment_list'),
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
        
        # imports urls 
        path('resa/ImportExcel_disease',imports.import_disease_recode, name="import_disease_recode"),
        path('import-insurance-companies/', imports.import_insurance_companies, name='import_insurance_companies'),
        path('import-companies/', imports.import_companies, name='import_companies'),
        path('import-patients/', imports.import_patient_records, name='import_patient_records'),
        path('import-pathology-records/', imports.import_pathology_records, name='import_pathology_records'),
        path('import-medicine-records/', imports.import_medicine_records, name='import_medicine_records'),
        path('import-procedure-records/', imports.import_procedure_records, name='import_procedure_records'),
        path('import-referral-records/', imports.import_referral_records, name='import_referral_records'),
        
        # edit urls 
        path('edit-patient-disease-save/<int:patient_disease_id>/edit/', editView.edit_patient_disease_save, name='edit_patient_disease_save'),
        path('edit-sample-test/<int:sample_id>/edit/', editView.edit_sample, name='edit_sample'),
        path('diagnostic-test/<int:test_id>/edit/', editView.edit_diagnostic_test, name='edit_diagnostic_test'),
        path('disease-records/<int:disease_id>/edit/', editView.edit_disease_record, name='edit_disease_record'),
        path('insurance-records/<int:insurance_id>/edit/', editView.edit_insurance, name='edit_insurance'),
        path('pathodology/<int:pathodology_id>/edit/', editView.edit_pathodology, name='edit_pathodology'),
        path('company/<int:company_id>/edit/', editView.edit_company, name='edit_company'), 
        path('Patient/<int:patient_id>/edit/', editView.edit_patient, name='edit_patient'),
        path('edit_procedure/', editView.edit_procedure, name='edit_procedure'), 
        path('edit_referral/', editView.edit_referral, name='edit_referral'), 
        path('Patient/<int:patient_id>/add/', views.appointment_view, name='appointment_view'), 
        path('patient-procedure-history/<str:mrn>/view/', views.patient_procedure_history_view, name='patient_procedure_history_view_mrn'), 
        path('edit_medicine/<int:medicine_id>/', editView.edit_medicine, name='edit_medicine'),        
        path('edit_inventory/<int:inventory_id>/', editView.edit_inventory, name='edit_inventory'),
        path('edit_medication_payment/<int:payment_id>/', editView.edit_medication_payment, name='edit_medication_payment'),
        
        
        # delete urls 
        path('delete-patient-disease/<int:patient_disease_id>/', delete.delete_patient_disease, name='delete_patient_disease'),
        path('delete-medication-payment/<int:payment_id>/', delete.delete_medication_payment, name='delete_medication_payment'),
        path('delete-diagnostic/test/<int:test_id>/', delete.delete_diagnostic_test, name='delete_diagnostic_test'),
        path('delete_medicine/<int:medicine_id>/', delete.delete_medicine, name='delete_medicine'),
        path('disease-records/<int:disease_id>/delete/', delete.delete_disease_record, name='delete_disease_record'),        
        path('insurance-records/<int:insurance_id>/delete/', delete.delete_insurance, name='delete_insurance'),        
        path('pathodology/<int:pathodology_id>/delete/', delete.delete_pathodology, name='delete_pathodology'),
        path('company/<int:company_id>/delete/', delete.delete_company, name='delete_company'),
        path('delete_staff/<int:staff_id>/', delete.delete_staff, name='delete_staff'),
        path('delete-patient/<int:patient_id>/', delete.delete_patient, name='delete_patient'),
        path('delete_procedure/', delete.delete_procedure, name='delete_procedure'),
        path('delete_inventory/<int:inventory_id>/', delete.delete_inventory, name='delete_inventory'),
        path('delete_referral/', delete.delete_referral, name='delete_referral'),
        path('delete_sample/<int:sample_id>/', delete.delete_sample, name='delete_sample'),
        path('delete_medication_payment/<int:payment_id>/', delete.delete_medication_payment, name='delete_medication_payment'),
]
