from datetime import date
from django.db.models import Sum,Max,Q
from django.utils import json, timezone
from datetime import timedelta
from django.shortcuts import render, redirect,get_object_or_404
from django.contrib import messages
from Account.models import ContactInfo, Nurse,Staff,Student,StudentVisit, MedicineInventory
from django.http import HttpResponse
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
import django.utils.json as json
import json

def nurse_dashboard(request):

    # Check Login
    if 'nurse_id' not in request.session:
        return redirect('nurse_login')

    # Logged-in Nurse
    nurse = Nurse.objects.get(
        nurse_id=request.session['nurse_id']
    )

    today = date.today()

    # Dashboard Statistics
    todays_visits_count = StudentVisit.objects.filter(
        date=today
    ).count()

    total_patients = StudentVisit.objects.values(
        'reg_no'
    ).distinct().count()

    chronic_patients_count = StudentVisit.objects.filter(
        chronic_illness="Yes"
    ).values(
        'reg_no'
    ).distinct().count()

    low_stock_count = MedicineInventory.objects.filter(
        quantity__lte=10
    ).count()

    # Recent Visits
    recent_visits = StudentVisit.objects.order_by(
        '-date',
        '-time'
    )[:10]

    context = {

        "page": "dashboard",

        "nurse": nurse,

        "todays_visits_count": todays_visits_count,

        "total_patients": total_patients,

        "chronic_patients_count": chronic_patients_count,

        "low_stock_count": low_stock_count,

        "recent_visits": recent_visits,

    }

    return render(
        request,
        "Nurse/nurse_dashboard.html",
        context
    )
def student_visit(request, reg_no):

    student = get_object_or_404(Student, reg_no=reg_no)

    if request.method == "POST":

        StudentVisit.objects.create(

            reg_no=student.reg_no,
            student_name=student.name,
            department=student.department,
            blood_group=student.blood_group,

            problem=request.POST.get("problem"),

            medicine=request.POST.get("medicine"),
            dosage=request.POST.get("dosage_mg"),
            staff_name=request.POST.get("staff_name"),

            chronic_illness=request.POST.get("chronic_illness")

        )

        messages.success(request, "Student visit saved successfully.")

        return redirect("student_search")

    medicines = MedicineInventory.objects.all().order_by("medicine_name")

    departments = Staff.objects.values("department").distinct().order_by("department")

    staffs = Staff.objects.all().order_by("department", "name")

    context = {

        "student": student,

        "medicines": medicines,

        "departments": departments,

        "staffs": staffs,

        "problems": StudentVisit.PROBLEM_CHOICES,

        "chronic_choices": StudentVisit.CHRONIC_CHOICES,

        "page": "student_visit"

    }

    return render(request, "Nurse/student_visit.html", context)
def student_search(request):

    reg_no = request.GET.get("reg_no")

    if reg_no:
        return redirect("student_visit", reg_no=reg_no)

    return render(request, "Nurse/student_search.html")
from django.db.models import Q

def visit_history(request):

    visits = StudentVisit.objects.all().order_by("-date", "-time")

    search_date = request.GET.get("date")
    problem = request.GET.get("problem")
    reg_no = request.GET.get("reg_no")

    if search_date:
        visits = visits.filter(date=search_date)

    if problem:
        visits = visits.filter(problem=problem)

    if reg_no:
        visits = visits.filter(reg_no__icontains=reg_no)

    context = {
        "visits": visits,
        "problems": StudentVisit.PROBLEM_CHOICES,
        "selected_problem": problem,
        "selected_date": search_date,
        "reg_no": reg_no,
        "page": "visit_history",
    }

    return render(request, "Nurse/visit_history.html", context)
def inventory(request):

    medicines = MedicineInventory.objects.all().order_by("medicine_name")

    search = request.GET.get("search")

    if search:
        medicines = medicines.filter(medicine_name__icontains=search)

    total_medicines = medicines.count()

    total_stock = medicines.aggregate(
        total=Sum("quantity")
    )["total"] or 0

    context = {
        "medicines": medicines,
        "search": search,
        "total_medicines": total_medicines,
        "total_stock": total_stock,
        "page": "inventory",
    }

    return render(request, "Nurse/inventory.html", context)
def chronic_illness(request):

    # -----------------------------
    # Update Follow-up & Remarks
    # -----------------------------
    if request.method == "POST":

        visit_id = request.POST.get("visit_id")

        try:
            visit = StudentVisit.objects.get(visit_id=visit_id)

            follow_up = request.POST.get("follow_up_days")

            if follow_up:
                visit.follow_up_days = int(follow_up)
            else:
                visit.follow_up_days = None

            visit.remarks = request.POST.get("remarks", "")

            visit.save()

            messages.success(
                request,
                "Follow-up details updated successfully."
            )

        except StudentVisit.DoesNotExist:

            messages.error(
                request,
                "Patient record not found."
            )

        return redirect("chronic_illness")

    # -----------------------------
    # Search
    # -----------------------------
    search = request.GET.get("search", "")

    latest_visits = (
        StudentVisit.objects
        .filter(chronic_illness="Yes")
        .values("reg_no")
        .annotate(latest_visit=Max("visit_id"))
    )

    latest_ids = [
        item["latest_visit"]
        for item in latest_visits
    ]

    visits = StudentVisit.objects.filter(
        visit_id__in=latest_ids
    ).order_by("-date", "-time")

    if search:

        visits = visits.filter(

            Q(reg_no__icontains=search) |
            Q(student_name__icontains=search)

        )

    today = timezone.now().date()

    total_patients = visits.count()

    upcoming = 0
    due_today = 0
    overdue = 0

    # -----------------------------
    # Calculate Follow-up Status
    # -----------------------------
    for visit in visits:

        visit.next_checkup = None
        visit.status = "No Follow-up"
        visit.message = "No Follow-up Required"

        if visit.follow_up_days:

            visit.next_checkup = (
                visit.date +
                timedelta(days=visit.follow_up_days)
            )

            remaining = (
                visit.next_checkup -
                today
            ).days

            if remaining > 0:

                visit.status = "Upcoming"

                visit.message = (
                    f"{remaining} day(s) remaining"
                )

                upcoming += 1

            elif remaining == 0:

                visit.status = "Today"

                visit.message = (
                    "Check-up Due Today"
                )

                due_today += 1

            else:

                visit.status = "Overdue"

                visit.message = (
                    f"{abs(remaining)} day(s) overdue"
                )

                overdue += 1

    context = {

        "visits": visits,

        "search": search,

        "total_patients": total_patients,

        "upcoming": upcoming,

        "due_today": due_today,

        "overdue": overdue,

        "page": "chronic_illness",

    }

    return render(
        request,
        "Nurse/chronic_illness.html",
        context
    )
def inventory_request(request):

    inventory = MedicineInventory.objects.all().order_by("medicine_name")

    context = {
        "inventory": inventory
    }

    return render(
        request,
        "Nurse/inventory_request.html",
        context
    )
def download_inventory_pdf(request):

    if request.method != "POST":
        return HttpResponse("Invalid Request")

    items_json = request.POST.get("items")
    remarks = request.POST.get("remarks", "")

    if not items_json:
        return HttpResponse("No items selected.")

    items = json.loads(items_json)

    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = 'attachment; filename="Inventory_Purchase_Request.pdf"'

    pdf = canvas.Canvas(response)

    width, height = pdf._pagesize
    y = height - 50

    # ===========================
    # Header
    # ===========================

    pdf.setFont("Helvetica-Bold", 16)
    pdf.drawCentredString(width / 2, y, "SHC STUDENT HEALTH CARE SYSTEM")

    y -= 20
    pdf.setFont("Helvetica", 12)
    pdf.drawCentredString(width / 2, y, "Sacred Heart College (Autonomous)")

    y -= 18
    pdf.drawCentredString(width / 2, y, "Tirupattur - 635601")

    y -= 30
    pdf.setFont("Helvetica-Bold", 14)
    pdf.drawCentredString(width / 2, y, "INVENTORY PURCHASE REQUEST")

    y -= 20
    pdf.line(40, y, 560, y)

    # ===========================
    # Date
    # ===========================

    from datetime import datetime

    y -= 25
    pdf.setFont("Helvetica", 11)
    pdf.drawString(50, y, f"Date : {datetime.now().strftime('%d-%m-%Y %I:%M %p')}")

    y -= 30

    # ===========================
    # Table Header
    # ===========================

    pdf.setFont("Helvetica-Bold", 11)

    pdf.drawString(50, y, "No")
    pdf.drawString(100, y, "Item")
    pdf.drawString(430, y, "Quantity")

    y -= 10
    pdf.line(40, y, 560, y)

    y -= 20


    pdf.setFont("Helvetica", 11)

    for index, item in enumerate(items, start=1):

        pdf.drawString(50, y, str(index))
        pdf.drawString(100, y, item["item"])
        pdf.drawString(450, y, str(item["qty"]))

        y -= 20

        if y < 100:

            pdf.showPage()

            width, height = pdf._pagesize
            y = height - 50

            pdf.setFont("Helvetica-Bold", 11)
            pdf.drawString(50, y, "No")
            pdf.drawString(100, y, "Item")
            pdf.drawString(430, y, "Quantity")

            y -= 10
            pdf.line(40, y, 560, y)

            y -= 20
            pdf.setFont("Helvetica", 11)


    y -= 20

    pdf.setFont("Helvetica-Bold", 11)
    pdf.drawString(50, y, "Remarks")

    y -= 18

    pdf.setFont("Helvetica", 11)

    if remarks.strip():
        pdf.drawString(50, y, remarks)
    else:
        pdf.drawString(50, y, "Stock refill for Student Health Care Centre.")

    y -= 70

    pdf.line(60, y, 220, y)
    pdf.line(350, y, 510, y)

    pdf.drawString(95, y - 15, "Requested By")
    pdf.drawString(390, y - 15, "Approved By")

    pdf.setFont("Helvetica-Oblique", 9)
    pdf.drawCentredString(width / 2, 30, "Generated by SHC Student Health Care System")

    pdf.save()

    return response

def contact_enquiries(request):

    enquiries = ContactInfo.objects.all().order_by("-id")

    return render(
        request,
        "Nurse/contact_enquiries.html",
        {
            "enquiries": enquiries,
            "page": "contact_enquiries"
        }
    )
def nurse_logout(request):
    request.session.flush()
    storage = messages.get_messages(request)

    for _ in storage:
        pass

    return redirect("home")