from django.urls import path,include
from . import views
urlpatterns = [
    path('student_dashboard/', views.student_dashboard, name='student_dashboard'),
    path(
        "medical-visit/",
        views.medical_visit,
        name="medical_visit"
    ),

    path(
        "notice/",
        views.notice,
        name="notice"
    ),

    path(
        "logout/",
        views.student_logout,
        name="student_logout"
    ),
]