

from django.http import HttpResponseBadRequest, JsonResponse
from django.shortcuts import redirect, render,get_object_or_404
from .models import Company, DiagnosticTest, DiseaseRecode, InsuranceCompany, MedicationPayment, Medicine, MedicineInventory, PathodologyRecord, Patients, Procedure, Referral, Staffs
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction
from django.db.models import F

def delete_staff(request, staff_id):
    # Retrieve the staff object or return a 404 if not found
    staff = get_object_or_404(Staffs, id=staff_id)

    if request.method == 'POST':
        # Perform the deletion
        staff.delete()
        # Redirect to a success page or a list view
        messages.success(request, 'staff deleted successfully.')
        return redirect('manage_staff')  # Replace 'staff_list' with your actual list view name

    return render(request, 'delete/delete_staff_confirm.html', {'staff': staff})

def delete_patient(request, patient_id):
    # Retrieve the staff object or return a 404 if not found
    patient = get_object_or_404(Patients, id=patient_id)

    if request.method == 'POST':
        # Perform the deletion
        patient.delete()
        # Redirect to a success page or a list view
        messages.success(request, 'patient deleted successfully.')
        return redirect('manage_patient')  # Replace 'manage_patient' with your actual list view name

    return render(request, 'delete/delete_patient_confirm.html', {'patient': patient})

@csrf_exempt
@require_POST
def delete_medicine(request, medicine_id):
    # Get the medicine object or return 404 if not found
    medicine = get_object_or_404(Medicine, id=medicine_id)

    try:
        # Delete the medicine
        medicine.delete()
        message = f"Medicine '{medicine.name}' deleted successfully."
        return JsonResponse({'success': True, 'message': message})
    except Exception as e:
        # Handle any exception or error during deletion
        return JsonResponse({'success': False, 'message': str(e)})
    
def delete_insurance(request, insurance_id):
    insurance = get_object_or_404(InsuranceCompany, pk=insurance_id)

    if request.method == 'POST':
        try:
            # Delete the InsuranceCompany object
            insurance.delete()

            messages.success(request, 'Insurance details deleted successfully!')
            return redirect('manage_insurance')  # Replace 'your_redirect_url' with the appropriate URL name

        except Exception as e:
            messages.error(request, f'An error occurred: {e}')

    return render(request, 'delete/delete_insurance_confirmation.html', {'insurance': insurance})



@csrf_exempt  # Use csrf_exempt decorator for simplicity in this example. For a production scenario, consider using csrf protection.
def delete_procedure(request):
    if request.method == 'POST':
        try:
            procedure_id = request.POST.get('procedure_id')

            # Delete procedure record
            procedure_record = Procedure.objects.get(id=procedure_id)
            procedure_record.delete()

            return JsonResponse({'success': True, 'message': f'Procedure record for {procedure_record.name} deleted successfully.'})
        except Procedure.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Invalid procedure ID.'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': f'An error occurred: {e}'})

    return JsonResponse({'success': False, 'message': 'Invalid request method.'})

@csrf_exempt  # Use csrf_exempt decorator for simplicity in this example. For a production scenario, consider using csrf protection.
def delete_referral(request):
    if request.method == 'POST':
        try:
            referral_id = request.POST.get('referral_id')

            # Delete procedure record
            referral_record = Referral.objects.get(id=referral_id)
            referral_record.delete()

            return JsonResponse({'success': True, 'message': f'Referral record for {referral_record} deleted successfully.'})
        except Procedure.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Invalid Referral ID.'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': f'An error occurred: {e}'})

    return JsonResponse({'success': False, 'message': 'Invalid request method.'})


def delete_disease_record(request, disease_id):
    record = get_object_or_404(DiseaseRecode, pk=disease_id)

    if request.method == 'POST':
        try:
            # Delete the DiseaseRecode object
            record.delete()
            messages.success(request, 'Disease record deleted successfully!')
            return redirect('manage_disease')  # Replace with the appropriate URL name

        except Exception as e:
            messages.error(request, f'An error occurred: {e}')

    return render(request, 'delete/delete_disease_record_confirmation.html', {'record': record})

def delete_company(request, company_id):
    company = get_object_or_404(Company, pk=company_id)

    if request.method == 'POST':
        try:
            # Delete the Company object
            company.delete()

            messages.success(request, 'Company deleted successfully!')
            return redirect('manage_company')  # Replace 'your_redirect_url' with the appropriate URL name
        except Exception as e:
            messages.error(request, f'An error occurred: {e}')

    return render(request, 'delete/company_delete_confirmation_template.html', {'company': company})


def delete_pathodology(request, pathodology_id):
    pathodology = get_object_or_404(PathodologyRecord, pk=pathodology_id)

    if request.method == 'POST':
        try:
            # Delete the PathodologyRecord object
            pathodology.delete()

            messages.success(request, 'Pathodology record deleted successfully!')
            return redirect('manage_pathodology')  # Replace 'your_redirect_url' with the appropriate URL name

        except Exception as e:
            messages.error(request, f'An error occurred: {e}')

    return render(request, 'delete/pathodology_delete_confirmation.html', {'pathodology': pathodology})


    
@require_POST
def delete_inventory(request, inventory_id):
    # Get the MedicineInventory object
    inventory = get_object_or_404(MedicineInventory, pk=inventory_id)

    # Perform deletion
    inventory.delete()

    # Redirect to the medicine inventory page
    return redirect('medicine_inventory') 

@require_POST
def delete_diagnostic_test(request, test_id):
    # Get the MedicineInventory object
    test = get_object_or_404(DiagnosticTest, pk=test_id)

    # Perform deletion
    test.delete()

    # Redirect to the medicine inventory page
    return redirect('diagnostic_tests') 

   
@require_POST
def delete_medication_payment(request, payment_id):
    try:
        # Get the MedicationPayment object
        medication_payment = get_object_or_404(MedicationPayment, pk=payment_id)

        # Store the quantity being deleted for later adjustment
        deleted_quantity = medication_payment.quantity

        with transaction.atomic():
            # Perform deletion
            medication_payment.delete()

            # Adjust MedicineInventory
            MedicineInventory.objects.filter(medicine=medication_payment.medicine).update(
                quantity=F('quantity') + deleted_quantity
            )

        # Redirect to the MedicationPayment
        return redirect('medicine_inventory')

    except MedicationPayment.DoesNotExist:
        return HttpResponseBadRequest("MedicationPayment not found.")