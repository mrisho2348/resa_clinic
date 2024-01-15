from import_export import resources
from .models import Staffs

class StaffResources(resources.ModelResource):
    class Meta:
        model = Staffs
