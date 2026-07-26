from django.shortcuts import render, redirect
from Account.models import Staff

from Account.models import StudentVisit


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

    if "staff_id" not in request.session:
        return redirect("staff_login")

    staff = Staff.objects.get(staff_id=request.session["staff_id"])

    notices = StudentVisit.objects.filter(
        department=staff.department
    ).exclude(
        chronic_illness__iexact="No"
    ).exclude(
        chronic_illness__isnull=True
    ).exclude(
        chronic_illness=""
    ).order_by("-date")

    return render(request, "Staff/emergency_notice.html", {
        "staff": staff,
        "notices": notices,
        "page": "emergency_notice",
    })
def staff_logout(request):

    request.session.flush()

    return redirect("staff_login")