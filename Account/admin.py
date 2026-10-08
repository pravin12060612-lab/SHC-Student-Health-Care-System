from django.contrib import admin
from Account.models import MedicineInventory, Student, Staff, Nurse, StudentVisit,ContactInfo

# Register your models here.
admin.site.register(Student)
admin.site.register(Staff)
admin.site.register(Nurse)
admin.site.register(StudentVisit)
admin.site.register(MedicineInventory)
admin.site.register(ContactInfo)
