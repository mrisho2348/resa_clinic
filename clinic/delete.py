

from django.shortcuts import redirect, render,get_object_or_404
from .models import Staffs
from django.contrib import messages

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