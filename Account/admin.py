from django.contrib import admin
from Account.models import MedicineInventory, Student, Staff, Nurse, StudentVisit,ContactInfo


admin.site.site_header = "SHC Student Health Care System"
admin.site.site_title = "SHC Student Health Care"
admin.site.index_title = "SHC Administration Panel"
# Register your models here.
admin.site.register(Student)
admin.site.register(Staff)
admin.site.register(Nurse)
admin.site.register(StudentVisit)
admin.site.register(MedicineInventory)
admin.site.register(ContactInfo)
_original_index = admin.site.index

def custom_index(request, extra_context=None):
    response = _original_index(request, extra_context)
    return response