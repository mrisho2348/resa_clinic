
from django.urls import include, path

from . import views

urlpatterns = [
        path('',views.index, name="home"),
        path('resa/dashboard',views.dashboard, name="dashboard"),
        path('login', views.ShowLogin, name='login'), 
        path('logout_user', views.logout_user, name='logout_user'),  # Move this line here
        path('contact/', views.ContactFormView.as_view(), name='contact_form'),
        path('GetUserDetails', views.GetUserDetails, name='GetUserDetails'),
        path('dologin', views.DoLogin, name='DoLogin'),
        path('accounts/', include('django.contrib.auth.urls')),  
        path('resa/portfolio/details',views.portfolio_details, name="portfolio_details"),
        path('resa/contact',views.contact, name="contact"),
        path('resa/blog/single',views.blog_single, name="blog_single"),
        path('resa/page/404',views.page_404, name="page_404"),        
        path('resa/all-patients',views.manage_patient, name="manage_patient"),
        path('resa/consultation-queue',views.manage_consultation, name="manage_consultation"),
        path('resa/new-consultation',views.add_consultation, name="add_consultation"),
        path('resa/new-request',views.add_request, name="add_request"),
        path('resa/manage-company',views.manage_company, name="manage_company"),
        path('resa/manage-disease',views.manage_disease, name="manage_disease"),
        path('resa/manage-staff',views.manage_staff, name="manage_staff"),
        path('resa/resa-report',views.resa_report, name="resa_report"),
        path('resa/manage-insurance',views.manage_insurance, name="manage_insurance"),
        path('resa/manage-service',views.manage_service, name="manage_service"),
        path('resa/manage-adjustment',views.manage_adjustment, name="manage_adjustment"),
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
        path('resa/manage-pathodology',views.manage_pathodology, name="manage_pathodology"),
]
