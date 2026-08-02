from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.hashers import make_password
ph=RegexValidator(
        regex=r'^\d{10}$',
        message="Phone number must be 10 digits."
    )
class Student(models.Model):
    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    ]
    DEPARTMENT_CHOICES = [
        ('B.Sc CS', 'B.Sc Computer Science'),
        ('BCA', 'Bachelor of Computer Applications'),
        ('B.Com', 'Bachelor of Commerce'),
        ('BBA', 'Bachelor of Business Administration'),
        ('B.Sc Maths', 'B.Sc Mathematics'),
        ('B.Sc Physics', 'B.Sc Physics'),
        ('B.Sc Chemistry', 'B.Sc Chemistry'),
        ('B.Sc Zoology', 'B.Sc Zoology'),
        ('B.Sc Botany', 'B.Sc Botany'),
        ('BA English', 'BA English'),
        ('BA Tamil', 'BA Tamil'),
    ]
    
    reg_no = models.CharField(max_length=20, primary_key=True,unique=True)
    password = models.CharField(max_length=255)
    def save(self, *args, **kwargs):
        # Hash only if the password isn't already hashed
        if not self.password.startswith("pbkdf2_"):
            self.password = make_password(self.password)

        super().save(*args, **kwargs)
    email = models.EmailField(max_length=100,unique=True,null=True,blank=True)
    name = models.CharField(max_length=100)
    department = models.CharField(max_length=100,choices=DEPARTMENT_CHOICES)
    Year = models.IntegerField()
    dob = models.DateField()
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    blood_group = models.CharField(max_length=5)
    phone = models.CharField(max_length=15, validators=[ph],unique=True)
    parent_phone = models.CharField(max_length=15, validators=[ph],unique=True)

    def __str__(self):
        return self.name


class Staff(models.Model):
    staff_id = models.CharField(max_length=20, primary_key=True,unique=True)
    password = models.CharField(max_length=255)
    email = models.EmailField(max_length=100,unique=True,null=True,blank=True)
    def save(self, *args, **kwargs):
        if not self.password.startswith("pbkdf2_"):
            self.password = make_password(self.password)
        super().save(*args, **kwargs)
    designation = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    department = models.CharField(max_length=100,choices=Student.DEPARTMENT_CHOICES)
    phone = models.CharField(max_length=15, validators=[ph],unique=True)
    def __str__(self):
        return self.name


class Nurse(models.Model):
    nurse_id = models.CharField(max_length=20, primary_key=True,unique=True)
    password = models.CharField(max_length=255)
    def save(self,*args, **kwargs):
        if not self.password.startswith("pbkdf2_"):
            self.password=make_password(self.password)
        super().save(*args,**kwargs)
    name = models.CharField(max_length=100)
    qualification = models.CharField(max_length=100)
    phone = models.CharField(max_length=15, validators=[ph],unique=True)

    def __str__(self):
        return self.name
class StudentVisit(models.Model):

    PROBLEM_CHOICES = [
        ("Fever", "Fever"),
        ("Headache", "Headache"),
        ("Cold & Cough", "Cold & Cough"),
        ("Stomach Pain", "Stomach Pain"),
        ("Body Pain", "Body Pain"),
    ]

    CHRONIC_CHOICES = [
        ("No", "No"),
        ("Yes", "Yes"),
    ]

    visit_id = models.AutoField(primary_key=True)
    reg_no = models.CharField(max_length=50)
    student_name = models.CharField(max_length=100)
    department = models.CharField(max_length=100)
    blood_group = models.CharField(max_length=10, blank=True, null=True)

    problem = models.CharField(
        max_length=100,
        choices=PROBLEM_CHOICES
    )

    medicine = models.CharField(max_length=255)

    staff_name = models.CharField(max_length=100, blank=True, null=True)

    remarks = models.TextField(blank=True, null=True)

    chronic_illness = models.CharField(
        max_length=3,
        choices=CHRONIC_CHOICES,
        default="No"
    )
    follow_up_days = models.PositiveIntegerField(blank=True,null=True)
    date = models.DateField(auto_now_add=True)
    time = models.TimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.reg_no} - {self.date}"
class MedicineInventory(models.Model):
    medicine_id = models.AutoField(primary_key=True)
    medicine_name = models.CharField(max_length=150, unique=True)
    quantity = models.PositiveIntegerField(default=0) # Current stock count
    expiry_date = models.DateField()
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.medicine_name} (Stock: {self.quantity})"

class ContactInfo(models.Model):

    name = models.CharField(max_length=100)

    email = models.EmailField(unique=True)

    phone = models.CharField(max_length=15)

    issue = models.CharField(max_length=200)

    message = models.TextField()

    def __str__(self):

        return self.name