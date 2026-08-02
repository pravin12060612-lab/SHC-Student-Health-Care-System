from django.shortcuts import render

from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.hashers import check_password
from .models import Student,Staff,Nurse,ContactInfo
def home(request):
    return render(request, "Account/home.html")
def about(request):
    nurse = Nurse.objects.first()
    return render(request, "Account/about.html", {"nurse": nurse})
def contact(request):
    return render(request, "Account/contact.html")
def stud_login(req):
    return render(req,'Account/stud_login.html')
def stud_valid(request):
     if request.method == "POST":

        reg_no = request.POST.get("username").strip()
        password = request.POST.get("password").strip()

        # Empty validation
        if not reg_no or not password:
            messages.error(request, "All fields are required.")
            return redirect("stud_login")

        try:
            student = Student.objects.get(reg_no=reg_no)

            if check_password(password, student.password):

                # Create Session
                request.session["student_regno"] = student.reg_no
                request.session["student_name"] = student.name

                messages.success(request, "Login Successful")

                return redirect("student_dashboard")

            else:
                messages.error(request, "Invalid Password")
                return redirect("stud_login")

        except Student.DoesNotExist:
            messages.error(request, "Register Number Not Found")
            return redirect("stud_login")

     return redirect("stud_login")


def staff(req):
    return render(req,'Account/staff_login.html')
def staff_login(request):

    if request.method == "POST":

        staff_id = request.POST.get("username", "").strip()
        password = request.POST.get("password", "").strip()

        # Empty validation
        if not staff_id or not password:
            messages.error(request, "All fields are required.")
            return redirect("staff_login")

        try:
            staff = Staff.objects.get(staff_id=staff_id)

            if check_password(password, staff.password):

                # Create Session
                request.session["staff_id"] = staff.staff_id
                request.session["staff_name"] = staff.name

                messages.success(request, "Login Successful")

                return redirect("staff_dashboard")

            else:
                messages.error(request, "Invalid Password")
                return redirect("staff_login")

        except Staff.DoesNotExist:
            messages.error(request, "Staff ID Not Found")
            return redirect("staff_login")

    return redirect("staff_login")
def nurse_login(request):

    return render(
        request,
        "Account/nurse_login.html",
        {
            "title": "Nurse Login"
        }
    )


# ===========================
# Nurse Login Validation
# ===========================

def nurse_login_validate(request):

    if request.method == "POST":

        nurse_id = request.POST.get("nurse_id").strip()
        password = request.POST.get("password").strip()

        # Empty validation
        if not nurse_id or not password:
            messages.error(request, "All fields are required.")
            return redirect("nurse_login")

        try:
            nurse = Nurse.objects.get(nurse_id=nurse_id)

            if check_password(password, nurse.password):

                # Create Session
                request.session["nurse_id"] = nurse.nurse_id
                request.session["nurse_name"] = nurse.name

                messages.success(request, "Login Successful")

                return redirect("nurse_dashboard")

            else:
                messages.error(request, "Invalid Password")
                return redirect("nurse_login")

        except Nurse.DoesNotExist:
            messages.error(request, "Nurse ID Not Found")
            return redirect("nurse_login")

    return redirect("nurse_login")

def contact(request):

    if request.method == "POST":

        ContactInfo.objects.create(

            name=request.POST.get("name"),

            email=request.POST.get("email"),

            phone=request.POST.get("phone"),

            issue=request.POST.get("issue"),

            message=request.POST.get("message")

        )

        return redirect("home")

    return render(
        request,
        "Account/contact.html"
    )