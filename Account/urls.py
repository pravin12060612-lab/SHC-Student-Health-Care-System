from django.contrib import admin
from django.urls import path
from . import views
urlpatterns = [
    path("",views.home,name="home"),
    path("about/",views.about,name="about"),
    path("contact/",views.contact,name="contact"),
    path("stud_login/",views.stud_login,name="stud_login"),
    path("stud_valid/",views.stud_valid,name="validation"),
    path("staff_login/",views.staff,name="staff_login"),
    path("staff_valid/",views.staff_login,name="staff_valid"),
    path("Nurse_login/",views.nurse_login,name="nurse_login"),
    path("nurse_login_validate/",views.nurse_login_validate,name="nurse_login_validate"),
   # path("admin12/",views.admin,name="admin")
]