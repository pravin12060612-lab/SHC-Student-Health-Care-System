from django.contrib import messages
from django.shortcuts import render, redirect
from Account.models import Staff
from django.utils import timezone
from Account.models import StudentVisit
from datetime import timedelta

def staff_dashboard(request):

    if "staff_id" not in request.session:
        return redirect("staff_login")

    staff = Staff.objects.get(staff_id=request.session["staff_id"])

    return render(request, "Staff/dashboard.html", {
        "staff": staff,
        "page": "dashboard",
    })

def student_visit(request):

    if "staff_id" not in request.session:
        return redirect("staff_login")

    staff = Staff.objects.get(staff_id=request.session["staff_id"])

    visits = StudentVisit.objects.filter(
        staff_name=staff.name
    ).order_by("-date", "-time")

    return render(request, "Staff/student_visit.html", {
        "staff": staff,
        "visits": visits,
        "page": "student_visit",
    })

def emergency_notice(request):
    staff_id = request.session.get("staff_id")

    if not staff_id:
        return redirect("staff_login")

    staff = Staff.objects.get(staff_id=staff_id)

    department_map = {
        "COMPUTER SCIENCE": ["COMPUTER SCIENCE", "B.Sc CS"],
        "COMPUTER APPLICATIONS": ["COMPUTER APPLICATIONS", "BCA"],
        "COMPUTER APPLICATION (MCA)": ["COMPUTER APPLICATION (MCA)", "BCA"],
        "MATHEMATICS": ["MATHEMATICS", "B.Sc Maths"],
        "PHYSICS": ["PHYSICS", "B.Sc Physics"],
        "CHEMISTRY": ["CHEMISTRY", "B.Sc Chemistry"],
        "TAMIL": ["TAMIL", "BA Tamil"],
        "ENGLISH": ["ENGLISH", "BA English"],
        "ECONOMICS": ["ECONOMICS", "B.Com"],
        "SOCIAL WORK (HRM)": ["SOCIAL WORK (HRM)"],
        "LIFE EDUCATION": ["LIFE EDUCATION"],
        "DATA SCIENCE": ["DATA SCIENCE"],
    }

    departments = department_map.get(
        staff.department,
        [staff.department]
    )

    visits = StudentVisit.objects.filter(
        chronic_illness="Yes",
        department__in=departments
    ).order_by("-date", "-time")

    notices = []

    today = timezone.localdate()

    for visit in visits:
        follow_up_days = visit.follow_up_days or 0
        follow_up_date = visit.date + timedelta(days=follow_up_days)
        days_remaining = (follow_up_date - today).days

        if days_remaining <= 0:
            status = "Follow-up Required"
        else:
            status = "Pending"

        notices.append({
            "reg_no": visit.reg_no,
            "student_name": visit.student_name,
            "department": visit.department,
            "chronic_illness": visit.chronic_illness,
            "follow_up_days": follow_up_days,
            "follow_up_date": follow_up_date,
            "days_remaining": days_remaining,
            "status": status,
        })

    context = {
        "staff": staff,
        "notices": notices,
        "page": "emergency_notice",
    }

    return render(request, "Staff/emergency_notice.html", context)
def staff_logout(request):

    storage = messages.get_messages(request)

    for _ in storage:
        pass

    return redirect("home")