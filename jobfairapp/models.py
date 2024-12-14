from django.db import models
from django.core.validators import MinLengthValidator
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

#Admin side Tables
"""
class admin_user_login(models.Model):
    username = models.EmailField(unique=True)
    password = models.TextField(validators=[MinLengthValidator(8)])

class adminchanges(models.Model):
    left_title = models.CharField(max_length=50)
    right_title = models.CharField(max_length=50)
    left_content = models.CharField(max_length=50)
    right_content = models.CharField(max_length=50)
    job_images = models.ImageField(upload_to=None)
"""

#college Registration

class CollegeRegistration(models.Model):
    college_user_id = models.CharField(max_length=50, unique=True)
    college_name = models.CharField(max_length=255, null=True, blank=True)
    college_location = models.CharField(max_length=255, null=True, blank=True)
    college_stream = models.CharField(max_length=255, null=True, blank=True)
    college_to_be = models.CharField(max_length=255, null=True, blank=True)
    college_type = models.CharField(max_length=255, null=True, blank=True)
    collegeMail = models.EmailField(unique=True, null=True, blank=True)  
    naac_accreditation = models.CharField(max_length=255, null=True, blank=True)
    number_of_dept = models.IntegerField(null=True, blank=True)  # Made this optional
    collegeNumber = models.CharField(max_length=50, null=True, blank=True)  # Fixed field name
    ug_students = models.CharField(max_length=50, null=True, blank=True)  # Optional field
    pg_students = models.CharField(max_length=50, null=True, blank=True)
    contact_type = models.CharField(max_length=50, null=True, blank=True)
    district = models.CharField(max_length=50, null=True, blank=True)
    principal_name = models.CharField(max_length=255, null=True, blank=True)
    principal_number = models.CharField(max_length=50, null=True, blank=True)
    principal_email = models.EmailField(unique=True, null=True, blank=True)  
    placement_officer_name = models.CharField(max_length=255, null=True, blank=True)
    placement_officer_email = models.EmailField(unique=True, null=True, blank=True)  
    placement_officer_Number = models.CharField(max_length=50, null=True, blank=True)
    password = models.CharField(max_length=50)

"""

class Registration(models.Model):
    full_name = models.CharField(max_length=100)
    dob = models.DateField()
    gender = models.CharField(max_length=20)
    department = models.CharField(max_length=20)
    college_name = models.CharField(max_length=100)
    passed_out = models.CharField(max_length=4)
    address = models.TextField()
    country_code = models.CharField(max_length=5)
    phone = models.CharField(max_length=20)

"""
#student Registration tables
class primary_table(models.Model):
    firstname = models.CharField(max_length=100)
    middlename = models.CharField(max_length=100)
    lastname = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=10)
    blood_group = models.CharField(max_length=5)

    permanant_house_no = models.CharField(max_length=50)
    permanant_street_name = models.CharField(max_length=100)
    permanant_landmark = models.CharField(max_length=100)
    permanant_country = models.CharField(max_length=50)
    permanant_state = models.CharField(max_length=50)
    permanant_city = models.CharField(max_length=50)
    permanant_pincode = models.CharField(max_length=10)

    present_house_no = models.CharField(max_length=50)
    present_street_name = models.CharField(max_length=100)
    present_landmark = models.CharField(max_length=100)
    present_country = models.CharField(max_length=50)
    present_state = models.CharField(max_length=50)
    present_city = models.CharField(max_length=50)
    present_pincode = models.CharField(max_length=10)


    email = models.EmailField()
    alt_email = models.EmailField()
    mobile = models.CharField(max_length=15)
    alt_mobile = models.CharField(max_length=15, blank=True)


# 3rd Table
class AcademicDetails(models.Model):
    primary_table = models.ForeignKey(primary_table, on_delete=models.CASCADE)
    high_qualification = models.CharField(max_length=100)
    course_name = models.CharField(max_length=100,default='null')
    course_duration_start = models.DateField(null=True, blank=True)
    course_duration_end = models.DateField(null=True, blank=True)
    course_type = models.CharField(max_length=50,default='null')
    university_name = models.CharField(max_length=200,default='null')
    Specialization = models.CharField(max_length=100,default='null')
    grading_system = models.CharField(max_length=50,default='null')
    grading_marks = models.FloatField(default='null')


# 5th Table
class GraduateDetails(models.Model):
    primary_table = models.ForeignKey(primary_table, on_delete=models.CASCADE)
    course_name = models.CharField(max_length=100)
    course_duration_start = models.DateField()
    course_duration_end = models.DateField()
    course_type = models.CharField(max_length=50)
    university_name = models.CharField(max_length=200)
    department = models.CharField(max_length=100)
    grading_system = models.CharField(max_length=50)
    grading_marks = models.FloatField()

class XIIanddiploma(models.Model):
    primary_table = models.ForeignKey(primary_table, on_delete=models.CASCADE)
    relevent_course = models.CharField(max_length=200)
    
    # 12th Grade details
    board_of_education = models.CharField(max_length=100, null=True, blank=True)
    specialization = models.CharField(max_length=100, null=True, blank=True)
    school_name = models.CharField(max_length=200, null=True, blank=True)
    duration_start = models.DateField(null=True, blank=True)
    duration_end = models.DateField(null=True, blank=True)
    grading_system = models.CharField(max_length=50, null=True, blank=True)
    grading_marks = models.FloatField(null=True, blank=True)
    
    # Diploma details
    course_name = models.CharField(max_length=200, null=True, blank=True)
    diploma_specialization = models.CharField(max_length=100, null=True, blank=True)
    university = models.CharField(max_length=200, null=True, blank=True)
    diploma_duration_start = models.DateField(null=True, blank=True)
    diploma_duration_end = models.DateField(null=True, blank=True)
    course_type = models.CharField(max_length=50, null=True, blank=True)
    diploma_grading_system = models.CharField(max_length=50, null=True, blank=True)
    diploma_grading_marks = models.FloatField(null=True, blank=True)


# 7th Table (xth)
class XthDetails(models.Model):
    primary_table = models.ForeignKey(primary_table, on_delete=models.CASCADE)
    roll_no = models.CharField(max_length=50)
    school_name = models.CharField(max_length=200)
    board_of_education = models.CharField(max_length=100)
    duration_start = models.DateField()
    duration_end = models.DateField()
    grading_system = models.CharField(max_length=50)
    grading_marks = models.FloatField()


# 8th Table (Other Qualification)
class OtherQualification(models.Model):
    primary_table = models.ForeignKey(primary_table, on_delete=models.CASCADE)
    any_other_course = models.CharField(max_length=100)
    course_name = models.CharField(max_length=100)
    specialization = models.CharField(max_length=100)
    duration_start = models.DateField(null=True, blank=True)
    duration_end = models.DateField(null=True, blank=True)
    course_type = models.CharField(max_length=50)
    grading_system = models.CharField(max_length=50)
    grading_marks = models.FloatField(null=True, blank=True)


# 9th Table (Work Experience)
class WorkExperience(models.Model):
    primary_table = models.ForeignKey(primary_table, on_delete=models.CASCADE)
    have_experience = models.CharField(max_length=100)
    experience = models.CharField(max_length=100)
    company_name = models.CharField(max_length=100)
    employee_type = models.CharField(max_length=100)
    duration_from = models.DateField(null=True, blank=True)
    duration_to = models.DateField(null=True, blank=True)
    designation = models.CharField(max_length=100)
    annual_salary = models.DecimalField(max_digits=10, decimal_places=2,null=True, blank=True)


class ArrearDetails(models.Model):
    primary_table = models.ForeignKey(primary_table, on_delete=models.CASCADE)
    arrears = models.CharField(max_length=3, choices=[('yes', 'Yes'), ('no', 'No')], default='no')
    active_history_arrear = models.CharField(max_length=100)
    arrear_count = models.IntegerField(null=True, blank=True)


# 10th Table (Others)
class OtherDetails(models.Model):
    primary_table = models.ForeignKey(primary_table, on_delete=models.CASCADE)
    nationality = models.CharField(max_length=50)
    language = models.CharField(max_length=50)
    speak = models.BooleanField(default=False)
    read = models.BooleanField(default=False)
    write = models.BooleanField(default=False)
    mother_tongue = models.CharField(max_length=50)

# 11th Table (Photo/CV)
class PhotoCV(models.Model):
    primary_table = models.ForeignKey(primary_table, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='photos/')
    cv = models.FileField(upload_to='cvs/')
    password = models.CharField(max_length=50)
    payment_status = models.CharField(max_length=20, choices=[('Pending', 'Pending'), ('Completed', 'Completed'), ('Failed', 'Failed')])  # Payment status

    

#job fair registration
class Registration(models.Model):
    sno = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    aadhar_num = models.CharField(max_length=12, unique=True)
    pan_num = models.CharField(max_length=50, unique=True)
    email = models.CharField(max_length=50, unique=True)


class jobfair_login(models.Model):
    Registration = models.ForeignKey(Registration, on_delete=models.CASCADE)
    qualification = models.CharField(max_length=100)
    department = models.CharField(max_length=100)
    select_level = models.CharField(max_length=100)
    email = models.CharField(max_length=50, unique=True)
    phone_number = models.CharField(max_length=50, unique=True)


class ApplicationForm(models.Model):
    # Personal Details
    Registration = models.ForeignKey(Registration, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    email = models.EmailField(unique=True)
    gender = models.CharField(max_length=10)
    father_name = models.CharField(max_length=100)
    mother_name = models.CharField(max_length=100)
    address = models.TextField()
    
    # Education Details - Graduation
    education_level = models.CharField(max_length=20)  # "Graduation" or "Diploma"
    degree = models.CharField(max_length=100, blank=True, null=True)
    institute_name = models.CharField(max_length=100, blank=True, null=True)
    degree_start_date = models.DateField(blank=True, null=True)
    degree_end_date = models.DateField(blank=True, null=True)
    degree_percentage = models.FloatField(blank=True, null=True)
    
    # Education Details - Diploma
    diploma_name = models.CharField(max_length=100, blank=True, null=True)
    diploma_institute_name = models.CharField(max_length=100, blank=True, null=True)
    diploma_start_date = models.DateField(blank=True, null=True)
    diploma_end_date = models.DateField(blank=True, null=True)
    diploma_percentage = models.FloatField(blank=True, null=True)
    
    # 10th Grade Details
    school_name_10th = models.CharField(max_length=100)
    board_10th = models.CharField(max_length=100)
    start_date_10th = models.DateField()
    end_date_10th = models.DateField()
    percentage_10th = models.FloatField(blank=True, null=True)
    marks_10th = models.FloatField(blank=True, null=True)
    
    # 12th Grade Details
    school_name_12th = models.CharField(max_length=100)
    board_12th = models.CharField(max_length=100)
    start_date_12th = models.DateField()
    end_date_12th = models.DateField()
    percentage_12th = models.FloatField(blank=True, null=True)
    marks_12th = models.FloatField(blank=True, null=True)
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    
class ExamResult(models.Model):
    Registration = models.ForeignKey(Registration, on_delete=models.CASCADE)
    username = models.CharField(max_length=100, unique=True)  # To store the username
    marks = models.FloatField()  # To store the marks obtained
    department = models.CharField(max_length=100)
    status = models.CharField(max_length=10, choices=[("Pass", "Pass"), ("Fail", "Fail")])  # To store pass/fail status
    company = models.CharField(max_length=500, blank=True, null=True, default="none")
    specialization = models.CharField(max_length=500)



class Appointment(models.Model):
    
    # Full name
    name = models.CharField(max_length=100)

    # Email address
    email = models.EmailField()

    # Phone number
    phone = models.CharField(max_length=15)

    # Address
    address = models.TextField()

    # Appointment date
    date = models.DateField()

    # Appointment time (hour and minutes)
    time = models.TimeField()

    # AM/PM selection
    am_pm = models.CharField(max_length=2, choices=[('AM', 'AM'), ('PM', 'PM')])

    def __str__(self):
        return f"{self.name} - {self.date} at {self.time} {self.am_pm}"




class Contact(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    subject = models.CharField(max_length=255)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


"""
class Register1(models.Model):
    Registration = models.ForeignKey(Registration, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    college_name = models.CharField(max_length=200)
    Degree = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=50, unique=True)
    college_code = models.CharField(max_length=100)
    email = models.EmailField()

class Payment(models.Model):
    Registration = models.ForeignKey(Registration, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)  # Payment amount
    date = models.DateTimeField(auto_now_add=True)  # Date and time of payment
    status = models.CharField(max_length=20, choices=[('Pending', 'Pending'), ('Completed', 'Completed'), ('Failed', 'Failed')])  # Payment status
    payment_method = models.CharField(max_length=50, choices=[('Credit Card', 'Credit Card'), ('Debit Card', 'Debit Card'), ('PayPal', 'PayPal'), ('Bank Transfer', 'Bank Transfer')])  # Payment method
    transaction_id = models.CharField(max_length=100, unique=True)  # Unique transaction ID

    def __str__(self):
        return f"Payment {self.transaction_id} - {self.status}"
    
    from django.db import models
"""