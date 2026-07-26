from django.urls import path
from . import views

urlpatterns = [

    path("dashboard/", views.staff_dashboard, name="staff_dashboard"),
    path("student-visit/", views.student_visit, name="staff_student_visit"),
    path("emergency-notice/", views.emergency_notice, name="emergency_notice"),
    path("logout/", views.staff_logout, name="staff_logout"),

]