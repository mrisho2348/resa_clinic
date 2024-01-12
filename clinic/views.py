from django.shortcuts import render
from django.contrib.auth import logout,login
from django.http import HttpResponse,HttpResponseRedirect
from django.template import loader
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_protect
from django.contrib import messages
from django.http import JsonResponse
from django.views.generic.edit import FormView
from django.contrib.messages.views import SuccessMessageMixin
from django.core.mail import send_mail
from clinic.emailBackEnd import EmailBackend
from clinic.models import ContactDetails
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

def manage_patient(request):
    return render(request,"hod_template/manage_patients.html")

def manage_consultation(request):
    return render(request,"hod_template/manage_consultation.html")

def add_consultation(request):
    return render(request,"hod_template/add_consultation.html")

def add_request(request):
    return render(request,"hod_template/add_request.html")

def manage_company(request):
    return render(request,"hod_template/manage_company.html")

def manage_disease(request):
    return render(request,"hod_template/manage_disease.html")

def manage_staff(request):
    return render(request,"hod_template/manage_staff.html")

def manage_insurance(request):
    return render(request,"hod_template/manage_insurance.html")

def resa_report(request):
    return render(request,"hod_template/resa_reports.html")
def manage_service(request):
    return render(request,"hod_template/manage_service.html")

def manage_adjustment(request):
    return render(request,"hod_template/manage_adjustment.html")

def reports_adjustments(request):
    return render(request,"hod_template/reports_adjustments.html")

def reports_by_visit(request):
    return render(request,"hod_template/reports_by_visit.html")


def reports_comprehensive(request):
    return render(request,"hod_template/reports_comprehensive.html")

def reports_patients_visit_summary(request):
    return render(request,"hod_template/reports_patients_visit_summary.html")

def reports_patients(request):
    return render(request,"hod_template/reports_patients.html")

def reports_service(request):
    return render(request,"hod_template/reports_service.html")

def reports_stock_ledger(request):
    return render(request,"hod_template/reports_stock_ledger.html")

def reports_stock_level(request):
    return render(request,"hod_template/reports_stock_level.html")

def reports_orders(request):
    return render(request,"hod_template/reports_orders.html")
def individual_visit(request):
    return render(request,"hod_template/reports_individual_visit.html")

def product_summary(request):
    return render(request,"hod_template/product_summary.html")
def manage_pathodology(request):
    return render(request,"hod_template/manage_pathodology.html")




