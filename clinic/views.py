import logging
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth import logout,login
from django.http import HttpResponse,HttpResponseRedirect
from django.template import loader
from django.shortcuts import render
from django.urls import reverse
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
from clinic.models import Company, ContactDetails, CustomUser, DiseaseRecode, InsuranceCompany, PathodologyRecord, Patient, Staffs
from clinic.resources import StaffResources
from tablib import Dataset
from django.views.decorators.http import require_POST
# Create your views here.
def index(request):
    return render(request,"index.html")

def dashboard(request):
    return render(request,"hod_template/home_content.html")
def contact(request):
    return render(request,"contact.html")
def blog_single(request):
    return render(request,"blog-single.html")
def page_404(request):
    return render(request,"404.html")


def ShowLogin(request):  
  return render(request,'login.html')



def DoLogin(request):
    if request.method != "POST":
        return HttpResponse("<h2>Method Not allowed</h2>")
    else:
        user = EmailBackend.authenticate(request, request.POST.get("email"), request.POST.get("password"))
        if user is not None:
            if not user.is_active:
                messages.error(request, "Your account is not active. Please contact the administrator for support.")
                return HttpResponseRedirect(reverse("login"))

            login(request, user)
            if user.user_type == "1":
                return HttpResponseRedirect(reverse("dashboard"))
            elif user.user_type == "2":
                return HttpResponseRedirect(reverse("dashboard"))             
            else:
                return HttpResponseRedirect(reverse("login"))
        else:
            messages.error(request, "Invalid Login Details")
            return HttpResponseRedirect(reverse("login"))
    
    
def GetUserDetails(request):
  user = request.user
  if user.is_authenticated:
    return HttpResponse("User : "+user.email+" usertype : " + user.usertype)
  else:
    return HttpResponse("Please login first")   
  
  
def logout_user(request):
  logout(request)
  return HttpResponseRedirect(reverse("home"))
    
class ContactFormView(SuccessMessageMixin, FormView):
    template_name = 'contact_form.html'
    form_class = None  # No Django form is used
    success_url = '/success/'  # Set the URL where users should be redirected on success
    success_message = "Your message was submitted successfully. We'll get back to you soon."

    def form_valid(self, form):
        try:
            # Process the form data
            your_name = self.request.POST.get('your_name')
            your_email = self.request.POST.get('your_email')
            your_subject = self.request.POST.get('your_subject', '')
            your_message = self.request.POST.get('your_message')

            # Save to the model (optional)
            ContactDetails.objects.create(
                your_name=your_name,
                your_email=your_email,
                your_subject=your_subject,
                your_message=your_message
            )

            # Send email to the administrator
            send_mail(
                f'New Contact Form Submission: {your_subject}',
                f'Name: {your_name}\nEmail: {your_email}\nMessage: {your_message}',
                'from@example.com',  # Sender's email address
                ['mrishohamisi2348@gmail.com'],  # Administrator's email address
                fail_silently=False,
            )

            messages.success(self.request, self.get_success_message())
            return self.form_valid_redirection(self.form_valid_redirect())
        except Exception as e:
            messages.error(self.request, f"An error occurred: {str(e)}")
            return self.form_invalid(self.get_form())

    def form_invalid(self, form):
        # Handle the case where the form is invalid
        return self.render_to_response(self.get_context_data(form=form))

    def form_valid_redirection(self, redirect_to):
        return self.render_to_response({'redirect_to': redirect_to})

    def form_valid_redirect(self):
        return self.get_success_url()    


def portfolio_details(request):
    return render(request,"portfolio-details.html")

@login_required
def manage_patient(request):
    return render(request,"hod_template/manage_patients.html")

@login_required
def manage_consultation(request):
    return render(request,"hod_template/manage_consultation.html")

@login_required
def add_consultation(request):
    return render(request,"hod_template/add_consultation.html")

@login_required
def add_request(request):
    return render(request,"hod_template/add_request.html")

@login_required
def manage_company(request):
    companies=Company.objects.all() 
    return render(request,"hod_template/manage_company.html",{"companies":companies})

@login_required
def manage_disease(request):
    disease_records=DiseaseRecode.objects.all() 
    return render(request,"hod_template/manage_disease.html",{"disease_records":disease_records})

@login_required
def manage_staff(request):     
    staffs=Staffs.objects.all()  
    return render(request,"hod_template/manage_staff.html",{"staffs":staffs})  

@login_required
def manage_insurance(request):
    insurance_companies=InsuranceCompany.objects.all() 
    return render(request,"hod_template/manage_insurance.html",{"insurance_companies":insurance_companies})

@login_required
def resa_report(request):
    return render(request,"hod_template/resa_reports.html")

@login_required
def manage_service(request):
    return render(request,"hod_template/manage_service.html")

def manage_adjustment(request):
    return render(request,"hod_template/manage_adjustment.html")

@login_required
def reports_adjustments(request):
    return render(request,"hod_template/reports_adjustments.html")

@login_required
def reports_by_visit(request):
    return render(request,"hod_template/reports_by_visit.html")

@login_required
def reports_comprehensive(request):
    return render(request,"hod_template/reports_comprehensive.html")

@login_required
def reports_patients_visit_summary(request):
    return render(request,"hod_template/reports_patients_visit_summary.html")

@login_required
def reports_patients(request):
    return render(request,"hod_template/reports_patients.html")

@login_required
def reports_service(request):
    return render(request,"hod_template/reports_service.html")

@login_required
def reports_stock_ledger(request):
    return render(request,"hod_template/reports_stock_ledger.html")

def reports_stock_level(request):
    return render(request,"hod_template/reports_stock_level.html")

@login_required
def reports_orders(request):
    return render(request,"hod_template/reports_orders.html")

@login_required
def individual_visit(request):
    return render(request,"hod_template/reports_individual_visit.html")

@login_required
def product_summary(request):
    return render(request,"hod_template/product_summary.html")

@login_required
def manage_pathodology(request):
    pathodology_records=PathodologyRecord.objects.all() 
    return render(request,"hod_template/manage_pathodology.html",{"pathodology_records":pathodology_records})


logger = logging.getLogger(__name__)

@csrf_exempt
@login_required
def save_staff_view(request):
    if request.method == 'POST':
        try:
            # Retrieve form data from the POST request
            first_name = request.POST.get('firstName')
            middle_name = request.POST.get('middleName')
            lastname = request.POST.get('lastname')            
            gender = request.POST.get('gender')
            dob = request.POST.get('dob')
            phone = request.POST.get('phone')
            profession = request.POST.get('profession')            
            marital_status = request.POST.get('maritalStatus')
            email = request.POST.get('email')
            password = request.POST.get('password')            
            user_role = request.POST.get('userRole')

            # Create a new CustomUser instance (if not exists) and link it to Staffs
            user = CustomUser.objects.create_user(username=email, password=password, email=email, first_name=first_name, last_name=lastname, user_type=2)

            # Create a new Staffs instance and link it to the user
            
            user.staff.middle_name = middle_name
            user.staff.date_of_birth = dob
            user.staff.gender = gender            
            user.staff.phone_number = phone            
            user.staff.marital_status = marital_status
            user.staff.profession = profession
            user.staff.role = user_role
        
            # Save the staff record
            user.save()

            # For demonstration purposes, you can log the saved data
            logger.info(f'Data saved successfully: {user.staff.__dict__}')

            # Return a success response to the user
            return JsonResponse({'message': 'Data saved successfully'}, status=200)
        except Exception as e:
            # Handle exceptions and log the error
            logger.error(f'Error saving data: {str(e)}')
            return JsonResponse({'error': str(e)}, status=400)

    # Return an error response if the request is not POST
    return JsonResponse({'error': 'Invalid request method'}, status=405)
    
def update_staff_status(request):
    try:
        if request.method == 'POST':
            # Get the user_id and is_active values from POST data
            user_id = request.POST.get('user_id')
            is_active = request.POST.get('is_active')

            # Retrieve the staff object or return a 404 response if not found
            staff = get_object_or_404(CustomUser, id=user_id)

            # Toggle the is_active status based on the received value
            if is_active == '1':
                staff.is_active = False
            elif is_active == '0':
                staff.is_active = True
            else:
                messages.error(request, 'Invalid request')
                return redirect('manage_staff')  # Make sure 'manage_staffs' is the name of your staff list URL

            staff.save()
            messages.success(request, 'Status updated successfully')
        else:
            messages.error(request, 'Invalid request method')
    except Exception as e:
        messages.error(request, f'An error occurred: {str(e)}')

    # Redirect back to the staff list page
    return redirect('manage_staff')  # Make sure 'manage_staffs' is the name of your staff list URL

def edit_staff(request, staff_id):
    # Check if the staff with the given ID exists, or return a 404 page
    staff = get_object_or_404(Staffs, id=staff_id)  
    # If staff exists, proceed with the rest of the view
    request.session['staff_id'] = staff_id
    return render(request, "update/edit_staff.html", {"id": staff_id, "username": staff.admin.username, "staff": staff})   


def edit_staff_save(request):
    if request.method == "POST":
        try:
            # Retrieve the staff ID from the session
            staff_id = request.session.get('staff_id')
            if staff_id is None:
                messages.error(request, "Staff ID not found")
                return redirect("manage_staff")

            # Retrieve the staff instance from the database
            try:
                staff = Staffs.objects.get(id=staff_id)
            except ObjectDoesNotExist:
                messages.error(request, "Staff not found")
                return redirect("manage_staff")

            # Extract the form data
            first_name = request.POST.get('firstName')
            middle_name = request.POST.get('middleName')
            lastname = request.POST.get('lastname')            
            gender = request.POST.get('gender')
            dob = request.POST.get('date_of_birth')
            phone = request.POST.get('phone')
            profession = request.POST.get('profession')            
            marital_status = request.POST.get('maritalStatus')
            email = request.POST.get('email')                        
            user_role = request.POST.get('userRole')    
          

            # Save the staff details
   
            staff.admin.first_name = first_name
            staff.admin.last_name = lastname
            staff.admin.email = email
            staff.middle_name = middle_name
            staff.role = user_role
            staff.profession = profession
            staff.marital_status = marital_status
            staff.date_of_birth = dob
            staff.phone_number = phone
            staff.gender = gender      
            staff.save()

            # Assuming the URL name for the next editing form is "qualification_form"
            messages.success(request, "Staff details updated successfully.")
            return redirect("manage_staff")
        except Exception as e:
            messages.error(request, f"Error updating staff details: {str(e)}")

    return redirect("edit_staff",staff_id=staff_id)




def single_staff_detail(request, staff_id):
    staff = get_object_or_404(Staffs, id=staff_id)
    # Fetch additional staff-related data  
    context = {
        'staff': staff,
     
    }

    return render(request, "hod_template/staff_details.html", context)

def import_staff(request):
    if request.method == 'POST':
        form = ImportStaffForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                staff_resource = StaffResources()
                new_staffs = request.FILES['staff_file']
                
                # Use tablib to load the imported data
                dataset = Dataset()
                imported_data = dataset.load(new_staffs.read(), format='xlsx')  # Assuming you are using xlsx, adjust accordingly

                for data in imported_data:
                   
                    user = CustomUser.objects.create_user(username=data[2],
                                                          password=data[2], 
                                                          email=data[2], 
                                                          first_name=data[0],
                                                          last_name=data[1],
                                                          user_type=2)
                    user.staff.middle_name =data[3],
                    user.staff.date_of_birth = data[5]
                    user.staff.gender = data[4],           
                    user.staff.phone_number = data[8]            
                    user.staff.marital_status = data[6]
                    user.staff.profession = data[7]
                    user.staff.role =data[9]
                    user.save()

                messages.success(request, 'Staff data imported successfully!')
            except Exception as e:
                messages.error(request, f'An error occurred: {e}')

    else:
        form = ImportStaffForm()

    return render(request, 'hod_template/import_staff.html', {'form': form})

@csrf_exempt
@login_required
def add_disease(request):
    try:
        if request.method == 'POST':
            disease_name = request.POST.get('Disease')
            code = request.POST.get('Code')

            # Save data to the model
            DiseaseRecode.objects.create(disease_name=disease_name, code=code)

            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'error': 'Invalid request method'})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})
 
@csrf_exempt
@login_required    
def add_insurance_company(request):
    try:
        if request.method == 'POST':
            name = request.POST.get('Name')
            phone = request.POST.get('Phone')
            short_name = request.POST.get('Short_name')
            email = request.POST.get('Email')
            address = request.POST.get('Address')

            # Save data to the model
            InsuranceCompany.objects.create(
                name=name,
                phone=phone,
                short_name=short_name,
                email=email,
                address=address
            )

            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'error': 'Invalid request method'})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})    
 
@csrf_exempt
@login_required      
def add_company(request):
    try:
        if request.method == 'POST':
            name = request.POST.get('Name')
            code = request.POST.get('Code')
            category = request.POST.get('Category')

            # Save data to the model
            Company.objects.create(
                name=name,
                code=code,
                category=category
            )

            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'error': 'Invalid request method'})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})
 
@csrf_exempt
@login_required      
def add_pathodology_record(request):
    try:
        if request.method == 'POST':
            name = request.POST.get('Name')
            description = request.POST.get('Description')

            # Save data to the model
            PathodologyRecord.objects.create(
                name=name,
                description=description
            )

            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'error': 'Invalid request method'})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})    
    

@csrf_exempt
@login_required
def add_patient(request):
    if request.method == 'POST':
        try:
            # Extracting data from the POST request
            mrn_format = request.POST.get('mrn_format')
            first_name = request.POST.get('first_name')
            middle_name = request.POST.get('middle_name')
            last_name = request.POST.get('last_name')
            gender = request.POST.get('gender')
            age = request.POST.get('age')
            nationality = request.POST.get('nationality')
            patient_type = request.POST.get('patient_type')

            # Continue extracting other fields in a similar way
            company = request.POST.get('company')
            occupation = request.POST.get('occupation')
            phone = request.POST.get('phone')
            employee_number = request.POST.get('employee_number')
            date_of_first_employment = request.POST.get('date_of_first_employment')
            print(date_of_first_employment)
            long_time_illness = request.POST.get('long_time_illness')
            long_time_medication = request.POST.get('long_time_medication')
            osha_certificate = request.POST.get('osha_certificate') == 'true'
            osha_date = request.POST.get('osha_date')
            print(osha_date)
            insurance = request.POST.get('insurance')
            insurance_name = request.POST.get('insurance_name')
            insurance_number = request.POST.get('insurance_number')

            # Extract Emergency Contact fields
            emergency_contact_name = request.POST.get('emergency_contact_name')
            emergency_contact_relation = request.POST.get('emergency_contact_relation')
            emergency_contact_phone = request.POST.get('emergency_contact_phone')
            emergency_contact_mobile = request.POST.get('emergency_contact_mobile')

            # Extract Health Condition fields
            allergies = request.POST.get('allergies')
            allergies_notes = request.POST.get('allergies_notes')
            eye_condition = request.POST.get('eye_condition', '')
            eye_condition_notes = request.POST.get('eye_condition_notes')
            ent_conditions = request.POST.get('ent_conditions')
            ent_conditions_notes = request.POST.get('ent_conditions_notes')
            respiratory_conditions = request.POST.get('respiratory_conditions')
            respiratory_conditions_notes = request.POST.get('respiratory_conditions_notes')
            cardiovascular_conditions = request.POST.get('cardiovascular_conditions')
            cardiovascular_conditions_notes = request.POST.get('cardiovascular_conditions_notes')
            urinary_conditions = request.POST.get('urinary_conditions')
            urinary_conditions_notes = request.POST.get('urinary_conditions_notes')
            stomach_bowel_conditions = request.POST.get('stomach_bowel_conditions')
            stomach_bowel_conditions_notes = request.POST.get('stomach_bowel_conditions_notes')
            musculoskeletal_conditions = request.POST.get('musculoskeletal_conditions')
            musculoskeletal_conditions_notes = request.POST.get('musculoskeletal_conditions_notes')
            neuro_psychiatric_conditions = request.POST.get('neuro_psychiatric_conditions')
            neuro_psychiatric_conditions_notes = request.POST.get('neuro_psychiatric_conditions_notes')
            # Continue extracting other health condition fields in a similar way

            # Extract Family History fields
            family_allergies = request.POST.get('family_allergies')
            family_allergies_relationship = request.POST.get('family_allergies_relationship')
            family_allergies_comments = request.POST.get('family_allergies_comments')

            family_asthma_condition = request.POST.get('family_asthma_condition')
            family_asthma_condition_relationship = request.POST.get('family_asthma_condition_relationship')
            family_asthma_condition_comments = request.POST.get('family_asthma_condition_comments')

            family_lungdisease_conditions = request.POST.get('family_lungdisease_conditions')
            family_lungdisease_conditions_relationship = request.POST.get('family_lungdisease_conditions_relationship')
            family_lungdisease_conditions_comments = request.POST.get('family_lungdisease_conditions_comments')

            family_diabetes_conditions = request.POST.get('family_diabetes_conditions')
            family_diabetes_conditions_relationship = request.POST.get('family_diabetes_conditions_relationship')
            family_diabetes_conditions_comments = request.POST.get('family_diabetes_conditions_comments')

            family_cancer_conditions = request.POST.get('family_cancer_conditions')
            family_cancer_conditions_relationship = request.POST.get('family_cancer_conditions_relationship')
            family_cancer_conditions_comments = request.POST.get('family_cancer_conditions_comments')

            family_hypertension_conditions = request.POST.get('family_hypertension_conditions')
            family_hypertension_conditions_relationship = request.POST.get('family_hypertension_conditions_relationship')
            family_hypertension_conditions_comments = request.POST.get('family_hypertension_conditions_comments')

            family_heart_disease_conditions = request.POST.get('family_heart_disease_conditions')
            family_heart_disease_conditions_relationship = request.POST.get('family_heart_disease_conditions_relationship')
            family_heart_disease_conditions_comments = request.POST.get('family_heart_disease_conditions_comments')

            # Continue extracting other family history fields in a similar way

            # Extract Lifestyle fields
            smoking = request.POST.get('smoking')
            alcohol_consumption = request.POST.get('alcohol_consumption')
            weekly_exercise_frequency = request.POST.get('weekly_exercise_frequency')
            healthy_diet = request.POST.get('healthy_diet')
            stress_management = request.POST.get('stress_management')
            sufficient_sleep = request.POST.get('sufficient_sleep')


            # Create a new patient instance with the extracted data
            new_patient = Patient(
                mrn_format=mrn_format,
                first_name=first_name,
                middle_name=middle_name,
                last_name=last_name,
                gender=gender,
                age=age,
                nationality=nationality,
                patient_type=patient_type,
                # Assign other fields similarly
            )
            # Continue assigning other fields similarly for the new_patient instance
            new_patient.company = company
            new_patient.occupation = occupation
            new_patient.phone = phone
            new_patient.employee_number = employee_number
            new_patient.date_of_first_employment = date_of_first_employment
            new_patient.long_time_illness = long_time_illness
            new_patient.long_time_medication = long_time_medication
            new_patient.osha_certificate = osha_certificate
            new_patient.osha_date = osha_date
            new_patient.insurance = insurance
            new_patient.insurance_name = insurance_name
            new_patient.insurance_number = insurance_number

            # Continue assigning Emergency Contact fields
            new_patient.emergency_contact_name = emergency_contact_name
            new_patient.emergency_contact_relation = emergency_contact_relation
            new_patient.emergency_contact_phone = emergency_contact_phone
            new_patient.emergency_contact_mobile = emergency_contact_mobile

            # Continue assigning Health Condition fields
            new_patient.allergies = allergies
            new_patient.allergies_notes = allergies_notes
            new_patient.eye_condition = eye_condition
            new_patient.eye_condition_notes = eye_condition_notes
            new_patient.ent_conditions = ent_conditions
            new_patient.ent_conditions_notes = ent_conditions_notes
            new_patient.respiratory_conditions = respiratory_conditions
            new_patient.respiratory_conditions_notes = respiratory_conditions_notes
            new_patient.cardiovascular_conditions = cardiovascular_conditions
            new_patient.cardiovascular_conditions_notes = cardiovascular_conditions_notes
            new_patient.urinary_conditions = urinary_conditions
            new_patient.urinary_conditions_notes = urinary_conditions_notes
            new_patient.stomach_bowel_conditions = stomach_bowel_conditions
            new_patient.stomach_bowel_conditions_notes = stomach_bowel_conditions_notes
            new_patient.musculoskeletal_conditions = musculoskeletal_conditions
            new_patient.musculoskeletal_conditions_notes = musculoskeletal_conditions_notes
            new_patient.neuro_psychiatric_conditions = neuro_psychiatric_conditions
            new_patient.neuro_psychiatric_conditions_notes = neuro_psychiatric_conditions_notes

            # Continue assigning Family History fields
            new_patient.family_allergies = family_allergies
            new_patient.family_allergies_relationship = family_allergies_relationship
            new_patient.family_allergies_comments = family_allergies_comments

            new_patient.family_asthma_condition = family_asthma_condition
            new_patient.family_asthma_condition_relationship = family_asthma_condition_relationship
            new_patient.family_asthma_condition_comments = family_asthma_condition_comments

            new_patient.family_lungdisease_conditions = family_lungdisease_conditions
            new_patient.family_lungdisease_conditions_relationship = family_lungdisease_conditions_relationship
            new_patient.family_lungdisease_conditions_comments = family_lungdisease_conditions_comments

            new_patient.family_diabetes_conditions = family_diabetes_conditions
            new_patient.family_diabetes_conditions_relationship = family_diabetes_conditions_relationship
            new_patient.family_diabetes_conditions_comments = family_diabetes_conditions_comments

            new_patient.family_cancer_conditions = family_cancer_conditions
            new_patient.family_cancer_conditions_relationship = family_cancer_conditions_relationship
            new_patient.family_cancer_conditions_comments = family_cancer_conditions_comments

            new_patient.family_hypertension_conditions = family_hypertension_conditions
            new_patient.family_hypertension_conditions_relationship = family_hypertension_conditions_relationship
            new_patient.family_hypertension_conditions_comments = family_hypertension_conditions_comments

            new_patient.family_heart_disease_conditions = family_heart_disease_conditions
            new_patient.family_heart_disease_conditions_relationship = family_heart_disease_conditions_relationship
            new_patient.family_heart_disease_conditions_comments = family_heart_disease_conditions_comments

            # Continue assigning Lifestyle fields
            new_patient.smoking = smoking
            new_patient.alcohol_consumption = alcohol_consumption
            new_patient.weekly_exercise_frequency = weekly_exercise_frequency
            new_patient.healthy_diet = healthy_diet
            new_patient.stress_management = stress_management
            new_patient.sufficient_sleep = sufficient_sleep       


            # Save the new patient instance to the database
            new_patient.save()
            
            logger.info(f'Data saved successfully: {new_patient.__dict__}')
            # Redirect to a success page or any other page as needed
            return JsonResponse({'message': 'Data saved successfully'}, status=200)

        except Exception as e:
            # Handle exceptions, you can log the error or redirect to an error page
            logger.error(f'Error saving data: {str(e)}')
            logger.error(f'Fields causing the error: {request.POST}')
            return JsonResponse({'error': str(e)}, status=400)
    return JsonResponse({'error': 'Invalid request method'}, status=405)    
      