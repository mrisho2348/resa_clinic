from datetime import date, datetime
import json
from django.utils import timezone
import logging
from django.db import models
from django.db import IntegrityError
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth import logout,login
from django.http import Http404, HttpResponse, HttpResponseBadRequest,HttpResponseRedirect
from django.template import loader
from django.shortcuts import render
from django.urls import reverse
from django.db.models import F
from django.views.decorators.csrf import csrf_protect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.views.generic.edit import FormView
from django.contrib.messages.views import SuccessMessageMixin
from django.core.mail import send_mail
from clinic.emailBackEnd import EmailBackend
from django.core.exceptions import ObjectDoesNotExist
from clinic.forms import ImportStaffForm
from clinic.models import RemoteCompany, Consultation, ContactDetails, CustomUser, DiseaseRecode, InsuranceCompany, Medicine, MedicineInventory, Notification, NotificationMedicine, PathodologyRecord, Patients, Procedure, Staffs
from clinic.resources import StaffResources
from tablib import Dataset
from django.views.decorators.http import require_POST
from django.contrib.contenttypes.models import ContentType
from django.db.models import OuterRef, Subquery
from .models import Category, ConsultationFee, ConsultationNotes, Country, Diagnosis, DiagnosticTest, Diagnosis, Equipment, EquipmentMaintenance, FamilyMedicalHistory, HealthIssue, InventoryItem, MedicationPayment, PathologyDiagnosticTest, PatientDisease, PatientHealthCondition, PatientVisits, PatientVital, Prescription, Procedure, Patients, QualityControl, Reagent, ReagentUsage, Referral, RemotePatient, RemotePatientVisits, RemotePrescription, Sample, Service, Supplier, UsageHistory

# Create your views here.
def index(request):
    return render(request,"index.html")

def labtechnician_dashboard(request):
    total_patients = Patients.objects.count()
    recently_added_patients = Patients.objects.order_by('-created_at')[:6]
    doctors = Staffs.objects.filter(role='doctor')
    context = {
        'total_patients': total_patients,
        'recently_added_patients': recently_added_patients,
        'doctors': doctors,
        # 'gender_based_monthly_counts': gender_based_monthly_counts,
    }
    return render(request,"receptionist_template/home_content.html",context)