from django.urls import path,include
from . import views
urlpatterns = [
    path('nurse_dashboard/', views.nurse_dashboard, name='nurse_dashboard'),
    path("student-visit/<str:reg_no>/", views.student_visit, name="student_visit"),
    path("student-search/", views.student_search, name="student_search"),
    path("visit-history/", views.visit_history, name="visit_history"),
    path("inventory/", views.inventory, name="inventory"),
    path("chronic-illness/",views.chronic_illness,name="chronic_illness"),
    path("inventory_request/",views.inventory_request,name="inventory_request"),
    path("download-inventory-pdf/",views.download_inventory_pdf,name="download_inventory_pdf"),
    path("contact-enquiries/",views.contact_enquiries,name="contact_enquiries"),
    path("logout/",views.nurse_logout,name="nurse_logout"),
    path("download-inventory-excel/", views.download_inventory_excel, name="download_inventory_excel"),
    path("download-visit-history-excel/", views.download_visit_history_excel, name="download_visit_history_excel"),
    path(
    "download-chronic-illness-excel/",
    views.download_chronic_illness_excel,
    name="download_chronic_illness_excel",
),
]