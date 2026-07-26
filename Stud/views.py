from django.http import request
from django.shortcuts import render
from datetime import timedelta
from django.utils import timezone

# Create your views here.
from django.shortcuts import render, redirect
from Account.models import Student,StudentVisit
def student_dashboard(request):

    if "student_regno" not in request.session:
        return redirect("stud_login")

    student = Student.objects.get(reg_no=request.session["student_regno"])

    return render(request, "Student/dashboard.html", {
        "student": student,
        "page": "dashboard",
        "total_visits": 0,
        "last_visit": "No Visits",
        "total_notices": 0,
    })


def medical_visit(request):

    if "student_regno" not in request.session:
        return redirect("stud_login")

    student = Student.objects.get(
        reg_no=request.session["student_regno"]
    )

    visits = StudentVisit.objects.filter(
        reg_no=student.reg_no
    ).order_by("-date", "-time")

    return render(request, "Student/medical_visit.html", {
        "student": student,
        "visits": visits,
        "page": "medical_visit",
    })

def notice(request):

    if "student_regno" not in request.session:
        return redirect("stud_login")

    student = Student.objects.get(reg_no=request.session["student_regno"])

    visit = StudentVisit.objects.filter(
        reg_no=student.reg_no
    ).order_by("-date").first()

    next_date = None
    remaining = None
    overdue_days = None

    if visit and visit.chronic_illness and visit.follow_up_days:

        next_date = visit.date + timedelta(days=int(visit.follow_up_days))

        remaining = (next_date - timezone.now().date()).days

        if remaining < 0:
            overdue_days = abs(remaining)

    return render(request, "Student/notice.html", {
        "student": student,
        "visit": visit,
        "next_date": next_date,
        "remaining": remaining,
        "overdue_days": overdue_days,
        "page": "notice",
    })
def student_logout(request):

    request.session.flush()

    return redirect("home")
