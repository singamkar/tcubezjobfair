from django.shortcuts import render,redirect
import random
from django.http import HttpResponse
from django.core.mail import send_mail
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from datetime import datetime
import os
from django.core.files.storage import FileSystemStorage
from .models import *
from django.core.paginator import Paginator
import pandas as pd
from datetime import datetime, timedelta
from .tasks import send_username_password_email

def generate_password(firstname):
    # Get the first two letters of the firstname (ensure lowercase or uppercase as needed)
    first_two_letters = firstname[:2].upper()  # or .lower() if you want lowercase
    # Get the current date and time
    current_datetime = datetime.now()
    date_str = current_datetime.strftime("%d")  # Two-digit day
    time_str = current_datetime.strftime("%H")  # Two-digit hour
    # Combine to form the password
    password = f"{first_two_letters}{date_str}{time_str}HR"
    return password

def generate_new_password(firstname):
    # Get the first two letters of the firstname (ensure lowercase or uppercase as needed)
    first_two_letters = firstname[1:3].upper()  # or .lower() if you want lowercase
    # Get the current date and time
    current_datetime = datetime.now()
    date_str = current_datetime.strftime("%d")  # Two-digit day
    time_str = current_datetime.strftime("%H")  # Two-digit hour
    # Combine to form the password
    password = f"{first_two_letters}{date_str}{time_str}HR"
    return password


def mailsend(mail_id):
    global otp
    otp = random.randint(1111,9999)
    subject = 'Otp verification'
    message = f'Your OTP for verification is: {otp}'
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [mail_id]

    send_mail(
        subject,
        message,
        from_email,
        recipient_list,
        otp,
    )

def home_view(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        from_email = settings.DEFAULT_FROM_EMAIL

        admin_subject = f'Message From {name}: {subject}'
        admin_message = message + f"\n Mail ID : {email}"
        user_message = f'Thank you for your message, {name}.\n\nYou wrote:\n{message}'

        try:
            # Send email to admin
            send_mail(
                admin_subject,
                admin_message,
                from_email,
                [settings.DEFAULT_FROM_EMAIL],
                fail_silently=False,
            )

            # Send confirmation email to user
            send_mail(
                'Thank you for contacting us!',
                user_message,
                from_email,
                [email],
                fail_silently=False,
            )

            return render(request, 'index.html', {'success': 'Message sent successfully!'})

        except Exception as e:
            return render(request, 'index.html', {'error': 'There was an error sending your message.'})

    return render(request, 'index.html')

def personal_1(request):
    # Retrieve email from session
    email = request.session.get('email')
    context = {}

    # Check if a session email exists
    if email:
        try:
            # Try to retrieve existing user data if email exists in session
            user_data = primary_table.objects.get(email=email)
            context['user_data'] = user_data
        except primary_table.DoesNotExist:
            messages.warning(request, "No data found for this email.")
            context['user_data'] = None
    else:
        context['user_data'] = None

    if request.method == "POST":
        # Capture data from form submission
        data = {
            'firstname': request.POST.get('firstname'),
            'middlename': request.POST.get('middlename'),
            'lastname': request.POST.get('lastname'),
            'date_of_birth': request.POST.get('dob'),
            'gender': request.POST.get('gender'),
            'blood_group': request.POST.get('blood_group'),
            'permanant_house_no': request.POST.get('permHouseNo'),
            'permanant_street_name': request.POST.get('permStreet'),
            'permanant_landmark': request.POST.get('permArea'),
            'permanant_country': request.POST.get('permCountry'),
            'permanant_state': request.POST.get('permState'),
            'permanant_city': request.POST.get('permCity'),
            'permanant_pincode': request.POST.get('permPincode'),
            'present_house_no': request.POST.get('presHouseNo'),
            'present_street_name': request.POST.get('presStreet'),
            'present_landmark': request.POST.get('presArea'),
            'present_country': request.POST.get('presCountry'),
            'present_state': request.POST.get('presState'),
            'present_city': request.POST.get('presCity'),
            'present_pincode': request.POST.get('presPincode'),
            'email': request.POST.get('email'),
            'alt_email': request.POST.get('altEmail'),
            'mobile': request.POST.get('mobilePhone'),
            'alt_mobile': request.POST.get('altPhone')
        }

        # Replace existing record or create a new one
        if email:
            
            primary_table.objects.filter(email=email).update(**data)
        else:
            # Check for duplicate email or mobile
            if primary_table.objects.filter(email=data['email']).exists():
                return JsonResponse({'success': False, 'message': 'Email already exists!'})

            if primary_table.objects.filter(mobile=data['mobile']).exists():
                return JsonResponse({'success': False, 'message': 'Mobile number already exists!'})


            # Create a new record if no session email
            primary_table.objects.create(**data)
            # Set session email to the new user's email
            request.session['email'] = data['email']


        # Redirect to another view (e.g., academic view)
        return JsonResponse({'success': True, 'message': 'Form submitted successfully!'})


    return render(request, 'personal_1.html', context)

def academic(request):
    # Redirect to a success page after saving

    return render(request,'academic.html')


def college_registration(request):
    
    if 'userId' in request.POST:  
            user_id = request.POST.get('userId')
            password = request.POST.get('password')

            try:
                user = CollegeRegistration.objects.get(college_user_id=user_id, password=password)

                messages.success(request, 'Login successful!')
                return redirect('college_preview',user_id=user_id)
            except CollegeRegistration.DoesNotExist:
                messages.error(request, 'Invalid User ID or Password.')
                return redirect('college_registration')
    return render(request, 'college_register.html')

def college_registration_form(request):
    if request.method == "POST":
            college_name = request.POST.get('collegeName')
            college_location = request.POST.get('collegelocation')
            college_stream = request.POST.get('stream')
            college_to_be = request.POST.get('collegeto')
            naac_accreditation = request.POST.get('naacacreadation')
            principal_name = request.POST.get('principalName')
            principal_number = request.POST.get('principalNumber')
            principal_email = request.POST.get('principalMail')
            placement_officer_name = request.POST.get('placementOfficerName')
            placement_officer_number = request.POST.get('placementOfficerNumber')
            placement_officer_email = request.POST.get('placementOfficerMail')
            number_of_dept = request.POST.get('departments')
            ug_students = request.POST.get('totalStudentsUG')
            pg_students = request.POST.get('totalStudentsPG')
            college_mail = request.POST.get('collegeMail')
            college_number = request.POST.get('collegeNumber')
            college_type = request.POST.get('college_type')
            district = request.POST.get('district')
            password = request.POST.get('password')

            #user_id
            if college_name and principal_number and college_stream:
                college_user_id = (college_name[:3] + principal_number[:2] + college_stream[:2]).upper()
            else:
                college_user_id = None

            #password
            current_date = datetime.now().strftime("%d")
            current_time = datetime.now().strftime("%H%M")
            if college_name and principal_name:
                password = (college_name[:2] + current_date + current_time + principal_name[:2]).lower()
            else:
                password = None

            
            subject = 'Welcome - Your College Registration Details'
            message = f"""Dear { principal_name },

                        We are pleased to inform you that your college, { college_name }, has been successfully registered on our platform. Below are your login credentials for accessing your account.

                        **Login Credentials:**

                        - **College User ID**: { college_user_id }
                        - **Password**: { password }

                        Please use the above credentials to log in to our portal. For security purposes, we recommend changing your password after your first login.

                        You can log in at the following link: [Login Link]

                        If you have any questions or encounter any issues, please don't hesitate to reach out to us at [support_email] or contact our support team at [support_phone_number].

                        Thank you for joining us, and we look forward to working with you!

                        Best regards,  
                        [THE HR COMPANY] 
                        """
                            
            from_email = settings.DEFAULT_FROM_EMAIL
            recipient_list = [principal_email]

            send_mail(
                subject,
                message,
                from_email,
                recipient_list,
                fail_silently=False
            )

            print(f"Generated College User ID: {college_user_id}")
            print(f"Generated Password: {password}")

            # Check if email or phone number already exists
            if CollegeRegistration.objects.filter(collegeMail=college_mail).exists():
                messages.error(request, 'The College Email is already in use. Please use a different email.')
                return redirect('college_registration')

            if CollegeRegistration.objects.filter(collegeNumber=college_number).exists():
                messages.error(request, 'The College Phone Number is already in use. Please use a different phone number.')
                return redirect('college_registration')

            if CollegeRegistration.objects.filter(principal_email=principal_email).exists():
                messages.error(request, 'The Principal Email is already in use. Please use a different email.')
                return redirect('college_registration')

            if CollegeRegistration.objects.filter(principal_number=principal_number).exists():
                messages.error(request, 'The Principal Phone Number is already in use. Please use a different phone number.')
                return redirect('college_registration')

            if CollegeRegistration.objects.filter(placement_officer_email=placement_officer_email).exists():
                messages.error(request, 'The Placement Officer Email is already in use. Please use a different email.')
                return redirect('college_registration')

            if CollegeRegistration.objects.filter(placement_officer_Number=placement_officer_number).exists():
                messages.error(request, 'The Placement Officer Phone Number is already in use. Please use a different phone number.')
                return redirect('college_registration')

            # Save data if validation passes
            try:
                CollegeRegistration.objects.create(
                    college_user_id=college_user_id,
                    college_name=college_name,
                    college_location=college_location,
                    college_stream=college_stream,
                    college_to_be=college_to_be,
                    naac_accreditation=naac_accreditation,
                    principal_name=principal_name,
                    principal_number=principal_number,
                    principal_email=principal_email,
                    placement_officer_name=placement_officer_name,
                    placement_officer_Number=placement_officer_number,
                    placement_officer_email=placement_officer_email,
                    number_of_dept=number_of_dept,
                    ug_students=ug_students,
                    pg_students=pg_students,
                    collegeMail=college_mail,
                    collegeNumber=college_number,
                    college_type=college_type,
                    district=district,
                    password=password 
                )
                messages.success(request, f'College registration submitted successfully! and Your LOGIN credential send to your { principal_name } Mail')
                return redirect('college_registration')  # Redirect to a success page
            except Exception as e:
                messages.error(request, f'Error submitting the form: {e}')
                return redirect('college_registration')
    return render(request, 'college_registration_form.html')

# def registered_college_login(request):
#     if request.method == 'POST':
#         user_id = request.POST.get('userId')
#         password = request.POST.get('password')

#         # Authenticate the user manually
       
# def submit_college_details(request):
    print("kar")
    if request.method == 'POST':
        user_id = request.POST.get('userId')
        college_name = request.POST.get('collegeName')
        stream = request.POST.get('stream')
        district = request.POST.get('district')
        address = request.POST.get('address')
        contact_type = request.POST.get('contactType')
        number_of_dept = request.POST.get('departments')
        ug_students = request.POST.get('totalStudentsUG')
        pg_students = request.POST.get('totalStudentsPG')


def academic_qualification(request):
    # Retrieve email from session
    email = request.session.get('email')
    context = {}

    if email:
        try:
            # Fetch the primary table entry using the email
            primary_entry = primary_table.objects.get(email=email)
            print(primary_entry)
            # Check for existing graduate details related to this primary entry
            academic_data = AcademicDetails.objects.filter(primary_table=primary_entry).first()
            print(academic_data)
            context['academic_data'] = academic_data  # Add graduate data to context if it exists
        except primary_table.DoesNotExist:
            messages.warning(request, "No data found for this email.")
            context['academic_data'] = None
    else:
        # Set primary entry as None if no email is in session
        context['academic_data'] = None

   

    if request.method == "POST":
        current_date = datetime.now().date()

        # Capture academic details from form submission
        high_qualification = request.POST.get('highest-qualification')
        course_name = request.POST.get('course_name')
        course_duration_start = request.POST.get('course_duration_start')
        course_duration_end = request.POST.get('course_duration_end')
        course_type = request.POST.get('course_type')
        specializations = request.POST.get('specializations')
        grading_system = request.POST.get('grading_system')
        
        # Determine grading marks based on grading system
        grading_marks = request.POST.get('grading_marks_input_cgpa') if grading_system == 'cgpa' else request.POST.get('grading_marks_input_percentage')

        

        if high_qualification == "bachelor-degree":
            # If session email exists, update or create academic details
            if email:
                try:
                    # Try to retrieve the academic details for updating
                    academic_details = AcademicDetails.objects.get(primary_table=primary_entry)
                    # Update existing academic details
                    academic_details.high_qualification = high_qualification
                    academic_details.course_name = ""
                    academic_details.course_duration_start =current_date
                    academic_details.course_duration_end = current_date
                    academic_details.course_type = ""
                    academic_details.Specialization = ""
                    academic_details.grading_system = ""
                    academic_details.grading_marks = "0"
                    academic_details.university_name = ""


                    academic_details.save()

                except AcademicDetails.DoesNotExist:
                    # Create new academic details if none exist
                    AcademicDetails.objects.create(
                        primary_table=primary_entry,
                        high_qualification=high_qualification,
                        course_name="",
                        course_duration_start=current_date,
                        course_duration_end=current_date,
                        course_type="",
                        Specialization="",
                        grading_system="",
                        grading_marks="0",
                        university_name = ""


                    )
                
                return redirect('academic_graduate')
            else:
                messages.warning(request, "You Need to Fill the Personal Details Page")
                return redirect('personal_1')
        else:
            
            # If session email exists, update or create academic details
            if email:
                try:
                    # Try to retrieve the academic details for updating
                    academic_details = AcademicDetails.objects.get(primary_table=primary_entry)
                    # Update existing academic details
                    academic_details.high_qualification = high_qualification
                    academic_details.course_name = course_name
                    academic_details.course_duration_start = course_duration_start
                    academic_details.course_duration_end = course_duration_end
                    academic_details.course_type = course_type
                    academic_details.Specialization = specializations
                    academic_details.grading_system = grading_system
                    academic_details.grading_marks = grading_marks
                    # Validate required fields
                    if not all([high_qualification, course_name, course_duration_start, course_duration_end, course_type, grading_system]):
                        messages.warning(request,'Please fill in all required fields')
                    academic_details.save()

                except AcademicDetails.DoesNotExist:
                    # Create new academic details if none exist
                    AcademicDetails.objects.create(
                        primary_table=primary_entry,
                        high_qualification=high_qualification,
                        course_name=course_name,
                        course_duration_start=course_duration_start,
                        course_duration_end=course_duration_end,
                        course_type=course_type,
                        Specialization=specializations,
                        grading_system=grading_system,
                        grading_marks=grading_marks
                    )

                
                return redirect('academic_graduate')
            else:
                messages.warning(request, "You Need to Fill the Personal Details Page")
                return redirect('personal_1')

    return render(request, 'academic_qualification.html', context)

def academic_graduate(request):
    # Retrieve email from session
    email = request.session.get('email')
    context = {}

    # Check if session email exists
    if email:
        try:
            # Fetch the primary table entry using the email
            primary_entry = primary_table.objects.get(email=email)
            # Check for existing graduate details related to this primary entry
            graduate_data = GraduateDetails.objects.filter(primary_table=primary_entry).first()
            context['graduate_data'] = graduate_data  # Add graduate data to context if it exists
        except primary_table.DoesNotExist:
            messages.warning(request, "No data found for this email.")
            context['graduate_data'] = None
    else:
        # Set primary entry as None if no email is in session
        context['graduate_data'] = None

    if request.method == "POST":
        # Capture graduate details from form submission
        course_name = request.POST.get('course_name')
        course_duration_start = request.POST.get('course_duration_start')
        course_duration_end = request.POST.get('course_duration_end')
        course_type = request.POST.get('course_type')
        university_name = request.POST.get('university_college_name')
        department = request.POST.get('specializations')
        grading_system = request.POST.get('grading_system')
        
        # Determine grading marks based on grading system
        if grading_system == 'cgpa':
            grading_marks = request.POST.get('grading_marks_input_cgpa')
        else:
            grading_marks = request.POST.get('grading_marks_input_percentage')

        # Validate required fields
        if not all([course_name, course_duration_start, course_duration_end, course_type, university_name, grading_system]):
            messages.error(request, "Please Fill all the Field")

        # If session email exists, update or create graduate details
        if email:
            try:
                # Try to retrieve the graduate details for updating
                graduate_details = GraduateDetails.objects.get(primary_table=primary_entry)
                # Update existing graduate details
                graduate_details.course_name = course_name
                graduate_details.course_duration_start = course_duration_start
                graduate_details.course_duration_end = course_duration_end
                graduate_details.course_type = course_type
                graduate_details.university_name = university_name
                graduate_details.department = department
                graduate_details.grading_system = grading_system
                graduate_details.grading_marks = grading_marks
                graduate_details.save()
                
            except GraduateDetails.DoesNotExist:
                # Create new graduate details if none exist
                GraduateDetails.objects.create(
                    primary_table=primary_entry,
                    course_name=course_name,
                    course_duration_start=course_duration_start,
                    course_duration_end=course_duration_end,
                    course_type=course_type,
                    university_name=university_name,
                    department=department,
                    grading_system=grading_system,
                    grading_marks=grading_marks
                )
            
            return redirect('academic_xii_grade')
        else:
            messages.warning(request, "First you fill personal details page")
            return redirect('personal_1')

    return render(request, 'academic_graduate.html', context)

def academic_xii_grade(request):
    email = request.session.get('email')
    context = {}

    if email:
        try:
            primary_entry = primary_table.objects.get(email=email)
            # Fetch existing records for each course type
            xii_data = XIIanddiploma.objects.filter(primary_table=primary_entry, relevent_course='12thGrade').first()
            diploma_data = XIIanddiploma.objects.filter(primary_table=primary_entry, relevent_course='equivalentDiploma').first()

            context['xii_data'] = xii_data
            context['diploma_data'] = diploma_data
        except primary_table.DoesNotExist:
            messages.warning(request, "No data found for this email.")
            context['xii_data'] = None
            context['diploma_data'] = None
    else:
        context['xii_data'] = None
        context['diploma_data'] = None

    if request.method == "POST":
        course_type = request.POST.get('course')
        print(course_type)
        if course_type == '12thGrade':
            board_of_education = request.POST.get('boardSelection')
            specialization = request.POST.get('specialization12th')
            school_name = request.POST.get('school_name')
            duration_start = request.POST.get('durationFrom12th')
            duration_end = request.POST.get('durationTo12th')
            grading_marks = request.POST.get('cgpaObtained12th')

            if not all([board_of_education, specialization, school_name, duration_start, duration_end, grading_marks]):
                messages.error(request, "Please fill in all required fields.")

            # Either update the existing entry or create a new one
            xii_details, created = XIIanddiploma.objects.update_or_create(
                primary_table=primary_entry,
                defaults={
                    'relevent_course' : course_type,
                    'board_of_education': board_of_education,
                    'specialization': specialization,
                    'school_name': school_name,
                    'duration_start': duration_start,
                    'duration_end': duration_end,
                    'grading_system': 'percentage',
                    'grading_marks': grading_marks,
                    # Set diploma fields to 'None'
                    'course_name': 'None',
                    'diploma_specialization': 'None',
                    'university': 'None',
                    'diploma_duration_start': None,
                    'diploma_duration_end': None,
                    'course_type': 'None',
                    'diploma_grading_system': 'None',
                    'diploma_grading_marks': None,
                }
            )


            return redirect('academic_x_grade')

            


        elif course_type == 'equivalentDiploma':
            course_name = request.POST.get('Coursename')
            specialization = request.POST.get('specializationDiploma')
            university = request.POST.get('university')
            diploma_duration_start = request.POST.get('durationFromDiploma')
            diploma_duration_end = request.POST.get('durationToDiploma')
            course_type_value = request.POST.get('courseTypeDiploma')
            diploma_grading_marks = request.POST.get('marksObtainedDiploma')

            if not all([course_name, specialization, university, diploma_duration_start, diploma_duration_end, course_type_value, diploma_grading_marks]):
                messages.error(request, "Please fill in all required fields.")
            # Either update the existing entry or create a new one
            diploma_details, created = XIIanddiploma.objects.update_or_create(
                primary_table=primary_entry,
                defaults={
                    'relevent_course' : course_type,
                    'course_name': course_name,
                    'diploma_specialization': specialization,
                    'university': university,
                    'diploma_duration_start': diploma_duration_start,
                    'diploma_duration_end': diploma_duration_end,
                    'course_type': course_type_value,
                    'diploma_grading_system': 'percentage',
                    'diploma_grading_marks': diploma_grading_marks,
                    # Set 12th-grade fields to 'None'
                    'board_of_education': 'None',
                    'specialization': 'None',
                    'school_name': 'None',
                    'duration_start': None,
                    'duration_end': None,
                    'grading_system': 'None',
                    'grading_marks': None,
                }
            )

            return redirect('academic_x_grade')

        messages.error(request, "Invalid course selection.")
        return redirect('personal_1')

    return render(request, 'academic_xii_grade.html', context)

def appointment(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        date = request.POST.get('date')
        time = request.POST.get('time')  # Expected format: 'HH:MM' or 'HH:MM:SS'
        am_pm = request.POST.get('ampm')  # AM or PM

        try:
            if len(time.split(':')) == 2:  # If time is in 'HH:MM' format
                time += ':00'  # Append seconds
            normalized_time = datetime.strptime(time, "%H:%M:%S").time()
        except ValueError as e:
            return JsonResponse({'success': False, 'message': f'Invalid time format: {e}'})

        try:
            appointment_datetime = datetime.strptime(f"{date} {normalized_time}", "%Y-%m-%d %H:%M:%S")
        except ValueError as e:
            return JsonResponse({'success': False, 'message': f'Invalid date or time format: {e}'})

        # Get existing appointments for the same date and am_pm
        existing_appointments = Appointment.objects.filter(date=date, am_pm=am_pm)

        for existing in existing_appointments:
            # Combine existing appointment's date and time into a datetime object
            existing_datetime = datetime.combine(
                existing.date,  # This is already a datetime.date object
                existing.time   # This is already a datetime.time object
            )

            time_difference = abs((appointment_datetime - existing_datetime).total_seconds())
            if time_difference < 30 * 60:  # 30 minutes in seconds
                return JsonResponse({'success': False, 'message': 'This slot conflicts with an existing appointment. Please choose a time at least 30 minutes apart.'})

        Appointment.objects.create(
            name=name,
            email=email,
            phone=phone,
            address=address,
            date=date,
            time=normalized_time,
            am_pm=am_pm
        )

        # Construct the email subject and message
        admin_subject = f"Appointment From {name}"
        admin_message = (
            f"Appointment Details:\n"
            f"Name: {name}\n"
            f"Email: {email}\n"
            f"Phone: {phone}\n"
            f"Address: {address}\n"
            f"Date: {date}\n"
            f"Time: {time} {am_pm}\n"
        )

        # Send the email
        send_mail(
            subject=admin_subject,
            message=admin_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[settings.DEFAULT_FROM_EMAIL],
            fail_silently=False,
        )

        # Respond with a JSON success message
        return JsonResponse({'success': True, 'message': 'Form submitted successfully!'})

    # Render the form for GET requests
    return render(request, 'appointment.html')

def gallery(request):
    return render(request,"gallery.html")

def other_details(request):
    email = request.session.get('email')
    context = {}

    if email:
        try:
            primary_entry = primary_table.objects.get(email=email)
            other_details_data = OtherDetails.objects.filter(primary_table=primary_entry)
            context['other_details_data'] = other_details_data
        except primary_table.DoesNotExist:
            messages.warning(request, "You Need to Fill the Personal Details Page")
            context['other_details_data'] = None
    else:
        messages.error(request, "You Need to Fill the Personal Details Page")
        return redirect('personal_1')

    if request.method == "POST":
        nationality = request.POST.get('nationality')
        languages = request.POST.getlist('language')
        speaks = request.POST.getlist('speak')
        reads = request.POST.getlist('read')
        writes = request.POST.getlist('write')
        mother_tongues = request.POST.getlist('mother-tongue')

        if not nationality:
            messages.error(request, "Nationality is required.")
            return render(request, 'other_details.html', context)

        # Clear existing details to replace with updated data
        OtherDetails.objects.filter(primary_table=primary_entry).delete()

        languages_saved = False
        for i in range(len(languages)):
            print(f"Processing language: {languages[i]}")
            if languages[i]:
                speak = 1 if (i < len(speaks) and speaks[i] == 'on') else 0
                read = 1 if (i < len(reads) and reads[i] == 'on') else 0
                write = 1 if (i < len(writes) and writes[i] == 'on') else 0
                mother_tongue = languages[i] if (i < len(mother_tongues) and mother_tongues[i] == 'on') else ""
                
                print(f"Creating entry with speak: {speak}, read: {read}, write: {write}, mother_tongue: {mother_tongue}")

                OtherDetails.objects.create(
                    primary_table=primary_entry,
                    nationality=nationality,
                    language=languages[i],
                    speak=speak,
                    read=read,
                    write=write,
                    mother_tongue=mother_tongue
                )

                languages_saved = True

        print(f"languages_saved: {languages_saved}")

        if languages_saved:
            print("Redirecting to resume")
            return redirect('resume')  # Redirect on failure

        
        else:
            print("No languages selected.")

            messages.error(request, "No languages selected.")
            return redirect('other_details')  # Redirect on failure

    return render(request, 'other_details.html', context)

def other_qualification(request):
    # Retrieve email from session
    email = request.session.get('email')
    context = {}

    # Check if session email exists
    if email:
        try:
            # Fetch the primary table entry using the email
            primary_entry = primary_table.objects.get(email=email)
            # Check for existing other qualifications related to this primary entry
            other_qualification_data = OtherQualification.objects.filter(primary_table=primary_entry).first()
            context['other_qualification_data'] = other_qualification_data  # Add data to context if it exists
        except primary_table.DoesNotExist:
            messages.warning(request, "You Need to Fill Personal Details Page")
            context['other_qualification_data'] = None
    else:
        # Set primary entry as None if no email is in session
        context['other_qualification_data'] = None

    if request.method == "POST":
        # Capture other qualification details from form submission
        any_other_course = request.POST.get('other_course')
        course_name = request.POST.get('course_name') if any_other_course == 'yes' else ''
        specialization = request.POST.get('specialization') if any_other_course == 'yes' else ''
        duration_start = request.POST.get('duration_start') if any_other_course == 'yes' else None
        duration_end = request.POST.get('duration_end') if any_other_course == 'yes' else None
        course_type = request.POST.get('course_type') if any_other_course == 'yes' else ''
        grading_system = 'percentage' if any_other_course == 'yes' else ''
        grading_marks = request.POST.get('percentage') if any_other_course == 'yes' else None

        # Validate required fields
        if any_other_course == 'yes' and not all([course_name, specialization, duration_start, duration_end, course_type, grading_marks]):
            messages.error(request, "Please fill in all required fields.")

        # If session email exists, update or create other qualification details
        if email:
            try:
                # Try to retrieve the other qualifications for updating
                other_qualification_entry = OtherQualification.objects.get(primary_table=primary_entry)
                # Update existing other qualification details
                other_qualification_entry.any_other_course = any_other_course
                other_qualification_entry.course_name = course_name
                other_qualification_entry.specialization = specialization
                other_qualification_entry.duration_start = duration_start
                other_qualification_entry.duration_end = duration_end
                other_qualification_entry.course_type = course_type
                other_qualification_entry.grading_system = grading_system
                other_qualification_entry.grading_marks = grading_marks
                other_qualification_entry.save()
            except OtherQualification.DoesNotExist:
                # Create new other qualification details if none exist
                OtherQualification.objects.create(
                    primary_table=primary_entry,
                    any_other_course=any_other_course,
                    course_name=course_name,
                    specialization=specialization,
                    duration_start=duration_start,
                    duration_end=duration_end,
                    course_type=course_type,
                    grading_system=grading_system,
                    grading_marks=grading_marks,
                )

            return redirect('work_exp')
        else:
            messages.warning(request, "You need to fill the personal details page.")
            return redirect('personal_1')

    return render(request, 'other_qualification.html', context)

def academic_x_grade(request):
    # Retrieve email from session
    email = request.session.get('email')
    context = {}

    # Check if session email exists
    if email:
        try:
            # Fetch the primary table entry using the email
            primary_entry = primary_table.objects.get(email=email)
            # Check for existing 10th-grade details related to this primary entry
            x_grade_data = XthDetails.objects.filter(primary_table=primary_entry).first()
            context['x_grade_data'] = x_grade_data  # Add 10th-grade data to context if it exists
        except primary_table.DoesNotExist:
            messages.warning(request, "No data found for this email.")
            context['x_grade_data'] = None
    else:
        # Set primary entry as None if no email is in session
        context['x_grade_data'] = None

    if request.method == "POST":
        # Capture 10th-grade details from form submission
        roll_no = request.POST.get('roll_no')
        school_name = request.POST.get('university')
        board_of_education = request.POST.get('board_of_education')
        duration_start = request.POST.get('duration_start')
        duration_end = request.POST.get('duration_end')
        grading_system = 'percentage'
        grading_marks = request.POST.get('percentage')

        # Validate required fields
        if not all([roll_no, school_name, board_of_education, duration_start, duration_end, grading_marks]):
            messages.warning(request, "Please fill in all required fields")

        # If session email exists, update or create 10th-grade details
        if email:
            try:
                # Try to retrieve the 10th-grade details for updating
                x_grade_details = XthDetails.objects.get(primary_table=primary_entry)
                # Update existing 10th-grade details
                x_grade_details.roll_no = roll_no
                x_grade_details.school_name = school_name
                x_grade_details.board_of_education = board_of_education
                x_grade_details.duration_start = duration_start
                x_grade_details.duration_end = duration_end
                x_grade_details.grading_system = grading_system
                x_grade_details.grading_marks = grading_marks
                x_grade_details.save()

            except XthDetails.DoesNotExist:
                # Create new 10th-grade details if none exist
                XthDetails.objects.create(
                    primary_table=primary_entry,
                    roll_no=roll_no,
                    school_name=school_name,
                    board_of_education=board_of_education,
                    duration_start=duration_start,
                    duration_end=duration_end,
                    grading_system=grading_system,
                    grading_marks=grading_marks,
                )

            return redirect('other_qualificaion')
        else:
            messages.warning(request, "You need to Fill Personal details Page.")
            return redirect('personal_1')
            

    return render(request, 'academic_x_grade.html', context)

def work_exp(request):
    # Retrieve email from session
    email = request.session.get('email')
    context = {}

    # Check if session email exists
    if email:
        try:
            # Fetch the primary table entry using the email
            primary_entry = primary_table.objects.get(email=email)
            # Check for existing work experience related to this primary entry
            work_experience_data = WorkExperience.objects.filter(primary_table=primary_entry).first()
            context['work_experience_data'] = work_experience_data  # Add data to context if it exists
        except primary_table.DoesNotExist:
            messages.warning(request, "You Need to Fill the Personal Details Page")
            context['work_experience_data'] = None
    else:
        # Set primary entry as None if no email is in session
        context['work_experience_data'] = None

    if request.method == "POST":
        # Capture work experience details from form submission
        have_experience = request.POST.get('have_experience')
        company_name = request.POST.get('name') if have_experience == 'yes' else ''
        employee_type = request.POST.get('employee_type') if have_experience == 'yes' else ''
        duration_from = request.POST.get('duration_from') if have_experience == 'yes' else None
        duration_to = request.POST.get('duration_to') if have_experience == 'yes' else None
        designation = request.POST.get('designation') if have_experience == 'yes' else ''
        annual_salary = request.POST.get('annual_salary') if have_experience == 'yes' else None

        # Calculate experience in years if both dates are provided
        experience_years = None
        if have_experience == 'yes' and duration_from and duration_to:
            duration_from_date = datetime.strptime(duration_from, "%Y-%m-%d")
            duration_to_date = datetime.strptime(duration_to, "%Y-%m-%d")
            # Calculate the difference in years and months
            total_months = (duration_to_date.year - duration_from_date.year) * 12 + (duration_to_date.month - duration_from_date.month)
            experience_years = f"{total_months // 12} years and {total_months % 12} months"

        else:
            experience_years = 'None'

        # Validate required fields
        if have_experience == 'yes' and not all([company_name, employee_type, duration_from, duration_to, designation, annual_salary]):
            messages.warning(request, "Please fill in all required fields.")

        # If session email exists, update or create work experience details
        if email:
            try:
                # Try to retrieve the work experience entry for updating
                work_experience_entry = WorkExperience.objects.get(primary_table=primary_entry)
                # Update existing work experience details
                work_experience_entry.have_experience = have_experience
                work_experience_entry.company_name = company_name
                work_experience_entry.employee_type = employee_type
                work_experience_entry.duration_from = duration_from
                work_experience_entry.duration_to = duration_to
                work_experience_entry.designation = designation
                work_experience_entry.annual_salary = annual_salary
                work_experience_entry.experience = experience_years
                work_experience_entry.save()

            except WorkExperience.DoesNotExist:
                # Create new work experience details if none exist
                WorkExperience.objects.create(
                    primary_table=primary_entry,
                    have_experience=have_experience,
                    company_name=company_name,
                    employee_type=employee_type,
                    duration_from=duration_from,
                    duration_to=duration_to,
                    designation=designation,
                    annual_salary=annual_salary,
                    experience=experience_years,
                )

            return redirect('arrear')
        else:
            messages.warning(request, "You need to Fill personal ddetails page")
            return redirect('personal_1')

    return render(request, 'work_exp.html', context)

def arrear(request):
    # Retrieve email from session
    email = request.session.get('email')
    context = {}

    # Check if session email exists
    if email:
        try:
            # Fetch the primary table entry using the email
            primary_entry = primary_table.objects.get(email=email)
            # Check for existing arrear details related to this primary entry
            arrear_details = ArrearDetails.objects.filter(primary_table=primary_entry).first()
            context['arrear_details'] = arrear_details  # Add data to context if it exists
        except primary_table.DoesNotExist:
            messages.warning(request, "You Need to Fill the Personal Details Page.")
            context['arrear_details'] = None
    else:
        # Set arrear details as None if no email is in session
        context['arrear_details'] = None

    if request.method == "POST":
        # Capture arrear details from form submission
        arrear_status = request.POST.get('arrear_status')
        active_history_arrear = request.POST.get('Arrear') if arrear_status == 'yes' else ''
        arrear_count = request.POST.get('arrearcount') if arrear_status == 'yes' and active_history_arrear else None

        # Validate required fields if arrears exist
        if arrear_status == 'yes' and not active_history_arrear:
            messages.warning(request, "Please select an arrear type.")

        if arrear_status == 'yes' and active_history_arrear and arrear_count is None:
            messages.warning(request, "Please enter your arrear count.")

        # If session email exists, update or create arrear details
        if email:
            try:
                # Try to retrieve the arrear details entry for updating
                arrear_entry = ArrearDetails.objects.get(primary_table=primary_entry)
                # Update existing arrear details
                arrear_entry.arrears = arrear_status
                arrear_entry.active_history_arrear = active_history_arrear
                arrear_entry.arrear_count = arrear_count
                arrear_entry.save()

            except ArrearDetails.DoesNotExist:
                # Create new arrear details if none exist
                ArrearDetails.objects.create(
                    primary_table=primary_entry,
                    arrears=arrear_status,
                    active_history_arrear=active_history_arrear,
                    arrear_count=arrear_count,
                )

            return redirect('other_details')
        else:
            messages.warning(request, "You need to Fill the personal details page.")
            return redirect('personal_1')

    return render(request, 'arrear.html', context)

def resume(request):
    email = request.session.get('email')
    context = {}
    if email:
        try:
            primary_entry = primary_table.objects.get(email=email)
            first_name = primary_entry.firstname  # Assuming `firstname` field exists in `primary_table`
            print(primary_entry)
            
        except primary_table.DoesNotExist:
            messages.warning(request, "You need to Fill the Personal Details page")
            return redirect('personal_1')
    else:
        messages.warning(request, "You need to Fill the Personal Details page")
        return redirect('personal_1')
    
    if request.method == "POST":
        fs_photo = FileSystemStorage(location='static/photos/')
        fs_cv = FileSystemStorage(location='static/resumes/')
        photo = request.FILES.get('photo')
        cv = request.FILES.get('cv')

        # Validate photo and CV sizes and formats
        if not photo:
            messages.error(request, "Photo is required.")
            return render(request, 'resume.html', context)

        if photo.size > 200 * 1024:  # 200 KB max
            messages.error(request, "Photo size exceeds 200 KB.")
            return render(request, 'resume.html', context)

        if not photo.name.lower().endswith(('jpg', 'jpeg', 'png')):
            messages.error(request, "Invalid photo format. Only JPG, JPEG, or PNG allowed.")
            return render(request, 'resume.html', context)

        # Save photo and CV
        photo_name = f"{first_name}.jpg" if photo.name.lower().endswith('jpg') else f"{first_name}.jpeg"
        photo_path = fs_photo.save(photo_name, photo)

        if not cv:
            messages.error(request, "CV is required.")
            return render(request, 'resume.html', context)

        if cv.size > 500 * 1024:  # 500 KB max
            messages.error(request, "CV size exceeds 500 KB.")
            return render(request, 'resume.html', context)

        if not cv.name.lower().endswith(('pdf', 'doc', 'docx')):
            messages.error(request, "Invalid CV format. Only PDF, DOC, or DOCX allowed.")
            return render(request, 'resume.html', context)

        cv_name = f"{first_name}.pdf" if cv.name.lower().endswith('pdf') else f"{first_name}.docx"
        cv_path = fs_cv.save(cv_name, cv)

        password = generate_password(primary_entry.firstname)

        # Save the photo and CV data
        photo_cv_entry, created = PhotoCV.objects.update_or_create(
            primary_table=primary_entry,
            defaults={
                'photo': photo_path,
                'cv': cv_path,
                'password': password,
                'payment_status': 'Pending'
            }
        )
        return redirect('preview')

    return render(request, 'resume.html', context)

def preview(request):
    # Retrieve email from session
    email = request.session.get('email')
    
    # Check if an email exists in the session
    if not email:
        messages.error(request, "You need to fill the Personal Details page first.")
        return redirect('personal_1')
    
    # Attempt to retrieve the primary entry for the user
    try:
        primary_entry = primary_table.objects.get(email=email)
    except primary_table.DoesNotExist:
        messages.warning(request, "You need to fill the Personal Details page first.")
        return redirect('personal_1')
    
    # Check if all required related tables have values
    required_tables = {
        'Academic Details': primary_entry.academicdetails_set.exists(),
        'Graduate Details': primary_entry.graduatedetails_set.exists(),
        'XII and Diploma Details': primary_entry.xiianddiploma_set.exists(),
        'Xth Details': primary_entry.xthdetails_set.exists(),
        'Other Qualifications': primary_entry.otherqualification_set.exists(),
        'Work Experience': primary_entry.workexperience_set.exists(),
        'Arrear Details': primary_entry.arreardetails_set.exists(),
        'Other Details': primary_entry.otherdetails_set.exists(),
        'Photo and CV': primary_entry.photocv_set.exists(),
    }

    # Check if any required table is missing data
    missing_tables = [table for table, has_data in required_tables.items() if not has_data]
    
    if missing_tables:
        # Redirect back with a list of missing sections
        messages.error(request, f"The following sections are incomplete: Please complete Academic and Work Experience Details before previewing.")
        return redirect('academic')  # Redirect to the relevant starting page
    
    # Organize the user's related details
    user_detail = {
        'user_detail': primary_entry,
        'academic_details': primary_entry.academicdetails_set.all(),
        'graduate_details': primary_entry.graduatedetails_set.all(),
        'xii_and_diploma': primary_entry.xiianddiploma_set.all(),
        'xth_details': primary_entry.xthdetails_set.all(),
        'other_qualifications': primary_entry.otherqualification_set.all(),
        'work_experience': primary_entry.workexperience_set.all(),
        'arrear_details': primary_entry.arreardetails_set.first(),
        'other_details': primary_entry.otherdetails_set.first(),
        'photo_cv': primary_entry.photocv_set.first(),
    }

    context = {
        'user_details': [user_detail],
    }

    return render(request, 'student_preview.html', context)

def reg(request):

    if request.method == 'POST':
        try:
            # Get form data
            name = request.POST.get('Name').capitalize()
            aadhaar = request.POST.get('aadhar')
            pan = request.POST.get('pan').upper()
            email = request.POST.get('email')

            # Check if the email or Aadhaar or PAN already exists
            if Registration.objects.filter(aadhar_num=aadhaar).exists():
                return JsonResponse({'success': False, 'message': 'Aadhaar already exists!'})

            if Registration.objects.filter(pan_num=pan).exists():
                return JsonResponse({'success': False, 'message': 'PAN already exists!'})

            if Registration.objects.filter(email=email).exists():
                return JsonResponse({'success': False, 'message': 'EMAIL already exists!'})

            # Save the data to the Registration model
            registration = Registration(name=name, aadhar_num=aadhaar, pan_num=pan, email=email)
            registration.save()

            # Send email (OTP in this case)
            mailsend(email)

            # Redirect to OTP verification page (Assuming you have a 'reg_otp' URL)
            return JsonResponse({'success': True, 'message': 'OTP send to your email.'})
            

        except Exception as e:

            return JsonResponse({'success': False, 'message': f'An error occurred: {str(e)}'}, status=500)

    # If the request is GET, render the form page
    return render(request, 'reg.html')

def reg_login(request):
    if request.method == 'POST':
        
        qualification = request.POST.get('qualification')
        select_level = request.POST.get('level')

        department = None  # Default value for department

        if qualification == 'artsscience':
            if select_level == 'UG':
                department = request.POST.get('dept1')  # Arts/Science UG Department
            elif select_level == 'PG':
                department = request.POST.get('dept2')  # Arts/Science PG Department

        elif qualification == 'engineering':
            if select_level == 'UG':
                department = request.POST.get('dept3')  # Engineering UG Department
            elif select_level == 'PG':
                department = request.POST.get('dept4')  # Engineering PG Department

        
        mobile = request.POST.get('mobile')
        email = request.POST.get('email')



        # Debugging prints
        print('Qualification:', qualification)
        print('Level:', select_level)
        print('Department:',department)
        print('Mobile:', mobile)
        print('Email:', email)


        # Check if the phone number already exists in jobfair_login
        if jobfair_login.objects.filter(phone_number=mobile).exists():
            return JsonResponse({'success': False, 'message': 'Phone Number already exists!'})
        
        # Check if the phone number already exists in jobfair_login
        if jobfair_login.objects.filter(email=email).exists():
            return JsonResponse({'success': False, 'message': 'Email already exists!'})

        # Fetch registration details
        try:
            registration = Registration.objects.get(email=email)
        except Registration.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Enter the registred email here..'})

        # Create a new jobfair_login entry
        try:
            jobfair_login.objects.create(
                Registration=registration,
                qualification=qualification,
                department=department,
                select_level=select_level,
                phone_number=mobile,
                email=email,
            )
        except Exception as e:
            return JsonResponse({'success': False, 'message': f'An error occurred: {str(e)}'}, status=500)

        return JsonResponse({'success': True, 'message':'Loggin Successfully..'})


    # Render the form if not POST
    return render(request, 'reg_login.html')

def reg_otp(request):

    if request.method=="POST":
        one_time_pass1 = request.POST.get('otp1')
        one_time_pass2 = request.POST.get('otp2')
        one_time_pass3 = request.POST.get('otp3')
        one_time_pass4 = request.POST.get('otp4')
        one_time_pass = one_time_pass1 + one_time_pass2 + one_time_pass3 + one_time_pass4
        if str(otp) == one_time_pass:
            return JsonResponse({'status': 'success', 'message': 'OTP verified successfully!'})
        else:
            return JsonResponse({'status': 'error', 'message': 'Incorrect OTP. Please try again.'})
    return render(request,'reg_otp.html',{'otp': otp})

def jobfairregister(request):
    if request.method == 'POST':
        # Extract form data from the POST request
        name = request.POST.get('name')
        dob = request.POST.get('dob')
        email = request.POST.get('email')
        gender = request.POST.get('gender')
        father_name = request.POST.get('fatherName')
        mother_name = request.POST.get('motherName')
        address = request.POST.get('address')
        education_level = request.POST.get('educationLevel')

        # Graduation/Diploma fields
        degree = request.POST.get('degree')
        institute_name = request.POST.get('instituteName')
        degree_start_date = request.POST.get('degreestartdate')
        degree_end_date = request.POST.get('degreeenddate')
        degree_percentage = request.POST.get('degreepercentage')
        diploma_name = request.POST.get('diploma')
        diploma_institute_name = request.POST.get('diplomainstitutename')
        diploma_start_date = request.POST.get('startdate')
        diploma_end_date = request.POST.get('enddate')
        diploma_percentage = request.POST.get('diplomapercentage')

        # 10th grade fields
        school_name_10th = request.POST.get('schoolname10th')
        board_10th = request.POST.get('board10th')
        start_date_10th = request.POST.get('startdate10th')
        end_date_10th = request.POST.get('enddate10th')
        type_10th = request.POST.get('markstype10th')
        percentage_10th = request.POST.get('percentageobtained10th')
        marks_10th = request.POST.get('marksobtained10th')

        # 12th grade fields
        school_name_12th = request.POST.get('12thschoolname')
        board_12th = request.POST.get('board12th')
        start_date_12th = request.POST.get('12thstartdate')
        end_date_12th = request.POST.get('12thenddate')
        type_12th = request.POST.get('markstype12th')
        percentage_12th = request.POST.get('12thpercentage')
        marks_12th = request.POST.get('12thmark')

        password = generate_password(name)
        # Print values like print(name, dob)
       
        # Check if a Registration record exists for the user
        try:
            registration = Registration.objects.get(email=email)
        except Registration.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Registration not found for this email..'})

        try:
            print(name, dob, email, gender, father_name, mother_name, address, education_level,
            degree, institute_name, degree_start_date, degree_end_date, degree_percentage,
            diploma_name, diploma_institute_name, diploma_start_date, diploma_end_date,
            diploma_percentage, school_name_10th, board_10th, start_date_10th, end_date_10th,
            percentage_10th, marks_10th, school_name_12th, board_12th, start_date_12th,
            end_date_12th, percentage_12th, marks_12th,type_12th,type_10th)
            # Create and save the ApplicationForm instance
            # application_form = XIIanddiploma.objects.update_or_create()

            application_form = ApplicationForm(
                Registration=registration,
                name=name,
                date_of_birth=datetime.strptime(dob, "%Y-%m-%d").date(), 
                email=email,
                gender=gender,
                father_name=father_name,
                mother_name=mother_name,
                address=address,
                education_level=education_level,
                degree=degree,
                institute_name=institute_name,
                degree_start_date=datetime.strptime(degree_start_date, "%Y-%m-%d").date() if degree_start_date else None,
                degree_end_date=datetime.strptime(degree_end_date, "%Y-%m-%d").date() if degree_end_date else None,
                degree_percentage=float(degree_percentage) if degree_percentage else None,
                diploma_name=diploma_name,
                diploma_institute_name=diploma_institute_name,
                diploma_start_date=datetime.strptime(diploma_start_date, "%Y-%m-%d").date() if diploma_start_date else None,
                diploma_end_date=datetime.strptime(diploma_end_date, "%Y-%m-%d").date() if diploma_end_date else None,
                diploma_percentage=float(diploma_percentage) if diploma_percentage else None,
                school_name_10th=school_name_10th,
                board_10th=board_10th,
                start_date_10th=datetime.strptime(start_date_10th, "%Y-%m-%d").date(),
                end_date_10th=datetime.strptime(end_date_10th, "%Y-%m-%d").date(),
                percentage_10th=float(percentage_10th) if percentage_10th else None,
                marks_10th=float(marks_10th) if marks_10th else None,
                school_name_12th=(school_name_12th) if school_name_12th else "None" ,
                board_12th=(board_12th) if board_12th else "None" ,
                start_date_12th = datetime.strptime(start_date_12th, "%Y-%m-%d").date() if start_date_12th else datetime.today().date(),
                end_date_12th = datetime.strptime(end_date_12th, "%Y-%m-%d").date() if end_date_12th else datetime.today().date(),
                percentage_12th=float(percentage_12th) if percentage_12th else 0,
                marks_12th=float(marks_12th) if marks_12th else 0,
                password = password,
            )
            # Printing all the values
        
            application_form.save()

            
            # Send exam link email immediately
            subject = 'Your Exam Link'
            message = 'You have successfully registered! Your exam link is: <your_exam_link_here>'
            from_email = settings.DEFAULT_FROM_EMAIL
            recipient_list = [email]
            send_mail(subject, message, from_email, recipient_list)
            
            # Schedule username and password email for 9:00 AM the next morning
            # Assuming Celery is set up
            #send_username_password_email.apply_async(
                #args=[email],
                #eta=datetime.now() + timedelta(minutes=1)
                # eta=datetime.datetime.combine(
                #     datetime.datetime.now() + datetime.timedelta(days=1),
                #     datetime.time(9, 0)
                #)
            #)
            
            return JsonResponse({'success': True, 'message': 'Form submitted successfully!'})

        except Exception as e:
            return JsonResponse({'success': False, 'message': 'Error occurred during form submission.', 'error': str(e)})


    return render(request, 'page24.html')

def payment(request):
    return render(request, 'payment.html')
    
def success(request):
    return render(request, 'success.html')

def college_preview(request,user_id):

    college = CollegeRegistration.objects.get(college_user_id=user_id)

    context = {
        'college': college
    }

    return render(request, 'college_preview.html', context)

def student_corner(request):
    if 'email' in request.session:
        del request.session['email']  # Clear any existing session data

    if request.method == "POST":
        user_id = request.POST.get("userId")
        password = request.POST.get("password")

        try:
            # Check if the user exists in primary_table with the provided email as user ID
            primary_entry = primary_table.objects.get(email=user_id)

            # Check if the password in PhotoCV matches the provided password
            photo_cv_entry = PhotoCV.objects.get(primary_table=primary_entry)

            if photo_cv_entry.password == password:
                # Set session variables for the logged-in user
                request.session['email'] = primary_entry.email  # Save email in session
                return redirect("student_preview")  # Redirect to profile view after login
            else:
                messages.error(request, "Invalid password. Please try again.")
                return redirect("student_corner")

        except primary_table.DoesNotExist:
            messages.error(request, "Invalid User ID. Please try again.")
            return redirect("student_corner")
        except PhotoCV.DoesNotExist:
            messages.error(request, "User has not completed registration.")
            return redirect("student_corner")

    return render(request, 'studentscorner.html')

def student_preview(request):

    # Retrieve the logged-in user's email from the session
    user_email = request.session.get("email")
    try:
        # Fetch the primary table entry based on the session email
        primary_entry = primary_table.objects.get(email=user_email)

        # Fetch related data from other tables using ForeignKey relations
        academic_details = AcademicDetails.objects.filter(primary_table=primary_entry)
        graduate_details = GraduateDetails.objects.filter(primary_table=primary_entry)
        xii_diploma_details = XIIanddiploma.objects.filter(primary_table=primary_entry)
        xth_details = XthDetails.objects.filter(primary_table=primary_entry)
        other_qualification = OtherQualification.objects.filter(primary_table=primary_entry)
        work_experience = WorkExperience.objects.filter(primary_table=primary_entry)
        arrear_details = ArrearDetails.objects.filter(primary_table=primary_entry)
        other_details = OtherDetails.objects.filter(primary_table=primary_entry)
        photo_cv = PhotoCV.objects.filter(primary_table=primary_entry).first() 

        context = {
            "primary_entry": primary_entry,
            "academic_details": academic_details,
            "graduate_details": graduate_details,
            "xii_diploma_details": xii_diploma_details,
            "xth_details": xth_details,
            "other_qualification": other_qualification,
            "work_experience": work_experience,
            "arrear_details": arrear_details,
            "other_details": other_details,
            "photo_cv": photo_cv,
        }

        return render(request, "preview.html", context)
    except primary_table.DoesNotExist:
        # Handle the case where no primary_table entry exists
        return redirect('students_corner')

def clear_session_and_redirect(request):
    try:
        email = request.session.get('email')
        
        if not email:
            messages.warning(request, "No email found in session.")
            return redirect('login')

        # Fetch the primary_table entry using the email
        primary_entry = primary_table.objects.get(email=email)
        
        # Assuming PhotoCV is linked to primary_table; adjust the logic if needed
        photo_cv_entry = PhotoCV.objects.get(primary_table=primary_entry)

        # Compose the email
        subject = 'Register Details'
        message = f'Your Username: {primary_entry.email}\nPassword: {photo_cv_entry.password}'
        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = [primary_entry.email]

        # Send the email
        send_mail(
            subject,
            message,
            from_email,
            recipient_list,
            fail_silently=False,  # This will show any errors in sending email
        )
        
        # Clear the session email
        del request.session['email']
        
        
    except primary_table.DoesNotExist:
        messages.error(request, "User with this email does not exist.")
        return redirect('personal_1')  # Adjust redirect if needed
    
    except PhotoCV.DoesNotExist:
        messages.error(request, "Password details not found.")
        return redirect('personal_1')  # Adjust redirect if needed
    
    except Exception as e:
        messages.error(request, "An error occurred while sending the email.")
        print(e)  # For debugging, consider removing in production
    
    return redirect('home')

def college_detail_view(request, college_user_id):
    college = get_object_or_404(CollegeRegistration, college_user_id=college_user_id)
    return render(request, 'college_details.html', {'college': college})

def admin_page(request):
    colleges = CollegeRegistration.objects.all()
    jobfairs = ApplicationForm.objects.all()
    students = primary_table.objects.all()
    exam_results = ExamResult.objects.all()  

    return render(request, 'admin_page.html', {
        'colleges': colleges,
        'jobfairs': jobfairs,
        'students': students,
        'exam_results': exam_results,
    })

def view_application(request, application_id):
    
    application = get_object_or_404(ApplicationForm, pk=application_id)

    
    return render(request, 'jobfair_preview.html', {'application': application})

def jobfair_details(request,pk):

    jobfair = get_object_or_404(ApplicationForm, pk=pk)
    return render(request, 'jobfair_details.html', {'jobfair': jobfair})

def student_detail(request, student_id):
    student = get_object_or_404(primary_table, id=student_id)
    academic_details = AcademicDetails.objects.filter(primary_table=student)
    graduate_details = GraduateDetails.objects.filter(primary_table=student)
    diploma_details = XIIanddiploma.objects.filter(primary_table=student)
    xth_details = XthDetails.objects.filter(primary_table=student)
    other_qualifications = OtherQualification.objects.filter(primary_table=student)
    work_experiences = WorkExperience.objects.filter(primary_table=student)
    arrear_details = ArrearDetails.objects.filter(primary_table=student)
    other_details = OtherDetails.objects.filter(primary_table=student)
    photo_cv = PhotoCV.objects.filter(primary_table=student).first()
    context = {
        'student': student,
        'academic_details': academic_details,
        'graduate_details': graduate_details,
        'diploma_details': diploma_details,
        'xth_details': xth_details,
        'other_qualifications': other_qualifications,
        'work_experiences': work_experiences,
        'arrear_details': arrear_details,
        'other_details': other_details,
        'photo_cv': photo_cv,
    }
    return render(request, 'student_detail.html', context)

def exam_result_detail(request, id):
    result = get_object_or_404(ExamResult, id=id)
    return render(request, 'exam_result_detail.html', {
        'result': result,
    })

def load_questions_from_excel(department):
    # Path to the single Excel file with multiple sheets 
    excel_file_path = os.path.join(settings.BASE_DIR, 'static', 'excel', 'questions.xlsx')

    # Load the sheet for the selected department
    try:
        df = pd.read_excel(excel_file_path, sheet_name=department)  # Load specific sheet
        questions = df.to_dict(orient='records')  # Convert to list of dictionaries
        return questions
    except Exception as e:
        print(f"Error loading sheet for department {department}: {e}")
        return []  # Return an empty list if the sheet cannot be loaded 


def submit_exam(request):
    if request.method == 'POST':
        department = request.POST.get('department')  # Get department from the form
        username = request.POST.get('user')  # Get username or email from the form
        user_email = request.POST.get('username')  # Email of the user
        print("Submitting exam for user:", user_email, "in department:", department)

        # Fetch the Registration object using email
        registration = get_object_or_404(Registration, email=user_email)

        # Load the questions for the selected department from the Excel file
        questions = load_questions_from_excel(department)
        total_score = 0

        # Loop through the questions and calculate the score
        for i, question in enumerate(questions, start=1):
            question_key = f'q{i}'
            submitted_answer = request.POST.get(question_key)  
            correct_answer = question.get('correct_answer')
            print(correct_answer)
            print(submitted_answer)
            
            # Check if the submitted answer matches the correct answer
            if submitted_answer == correct_answer:
                total_score += 1

        # Determine pass or fail status based on the total score
        print(total_score)
        status = "Pass" if total_score >= 1 else "Fail"
        print(status)

        existing_exam_result = ExamResult.objects.filter(Registration=registration, department=department).first()

        if existing_exam_result:
            existing_exam_result.marks = total_score
            existing_exam_result.status = status
            existing_exam_result.save()
            messages.success(request, f"Exam updated successfully! Your score is {total_score}.")
        else:
            # Create a new record if no existing result is found
            ExamResult.objects.create(
                Registration=registration,  
                username=user_email, 
                marks=total_score,
                department=department,
                status=status,
                company='none',
            )


        if status == "Fail":
            payment_link = "https://yourpaymentgateway.com/payment-link"
            try:
                send_mail(
                    subject="Re-Exam Notification",
                    message=(
                        f"Dear {registration.name},\n\n"
                        f"You did not pass the exam for the {department} department.\n\n"
                        f"To reattempt the exam, please pay ₹200 using the link below:\n\n"
                        f"{payment_link}\n\n"
                        f"Once the payment is completed, new login credentials will be sent to you."
                    ),
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[user_email],
                    fail_silently=False,
                )
                messages.info(request, "Re-exam email sent successfully.")
            except Exception as e:
                print(f"Failed to send email: {e}")
                messages.error(request, "Failed to send re-exam email.")

        else:
            return redirect('company_selection',username=username,user_email=user_email)

        return redirect('exam_result', username=username, score=total_score, status=status,user_email=user_email)

    return render(request, 'exam.html')

def exam_result(request, username, score, status,user_email):
    context = {
        'username': username,  
        'score': score,        
        'status': status,
        'email' : user_email,
    }
    return render(request, 'exam_result.html', context)


def exam_login(request):
    context = {}
    if request.method == "POST":
        username = request.POST.get("Username")  # Fetch the username from the form
        password = request.POST.get("Password")  # Fetch the password from the form

        print("Username:", username, "Password:", password)

        try:
            # Validate the username and password in ApplicationForm
            user = ApplicationForm.objects.get(email=username, password=password)
            new_password = generate_new_password(user.name)
            user.password = new_password
            user.save()

            # Fetch the related jobfair_login details
            jobfair_user = jobfair_login.objects.filter(email=username).first()
            
            if jobfair_user:
                # Add department to the context
                context["department"] = jobfair_user.department
                context["jobfair_login"] = jobfair_user
                context["user"] = user
                context["username"] = username

                # Load department-specific questions
                questions = load_questions_from_excel(jobfair_user.department)
                if questions:
                    context["questions"] = questions
                else:
                    messages.error(request, "No questions found for the selected department.")
                    return render(request, "exam_login.html", context)

                # Render the exam page with the department and other details
                return render(request, "exam.html", context)
            else:
                messages.error(request, "Jobfair login details not found for the given email.")
        except ApplicationForm.DoesNotExist:
            # Handle invalid login credentials
            messages.error(request, "Invalid username or password. Please try again.")

    return render(request, "exam_login.html")

def company_selection(request, username, user_email):
    # Load Excel data
    excel_file = os.path.join(settings.BASE_DIR, 'static', 'excel', 'companies.xlsx')
    df = pd.read_excel(excel_file)
    companies = df.to_dict(orient='records')

    # Fetch exam result or return error if not found
    exam_result = get_object_or_404(ExamResult, username=user_email)

    if request.method == "POST":
        selected_companies = request.POST.getlist('companies')
        selected_specializations = request.POST.getlist('specializations')

        # Validate selections
        if len(selected_companies) > 2:
            extra_charge = 200
            return JsonResponse({
                "success": False,
                "message": f"You selected more than 2 companies. An extra charge of ₹{extra_charge} applies.",
                "extra_charge": extra_charge,
            })

        # Save the selections
        exam_result.company = ', '.join(selected_companies)
        exam_result.specialization = ', '.join(selected_specializations)
        exam_result.save()

        return JsonResponse({
            "success": True,
            "message": "Your selections have been successfully saved.",
            "username": user_email,
        })

    return render(request, 'company.html', {
        'companies': companies,
        'username': username,
        'email': user_email,
    })

def previewpage(request, usermail):
    try:
        # Fetch user details
        registration = get_object_or_404(Registration, email=usermail)
        application_form = get_object_or_404(ApplicationForm, Registration=registration)
        exam_result = get_object_or_404(ExamResult, username=usermail)

        # Prepare context
        context = {
            "personal_details": {
                "name": registration.name,
                "aadhar_num": registration.aadhar_num,
                "pan_num": registration.pan_num,
                "email": registration.email,
                "gender": application_form.gender,
                "father_name": application_form.father_name,
                "mother_name": application_form.mother_name,
                "address": application_form.address,
                "degree": application_form.degree,
                "institute_name": application_form.institute_name,
                "degree_start_date": application_form.degree_start_date,
                "degree_end_date": application_form.degree_end_date,
                "degree_percentage": application_form.degree_percentage,
                "diploma_name": application_form.diploma_name,
                "diploma_institute_name": application_form.diploma_institute_name,
                "diploma_start_date": application_form.diploma_start_date,
                "diploma_end_date": application_form.diploma_end_date,
                "diploma_percentage": application_form.diploma_percentage,
                "school_name_10th": application_form.school_name_10th,
                "board_10th": application_form.board_10th,
                "start_date_10th": application_form.start_date_10th,
                "end_date_10th": application_form.end_date_10th,
                "percentage_10th": application_form.percentage_10th,
                "marks_10th": application_form.marks_10th,
                "school_name_12th": application_form.school_name_12th,
                "board_12th": application_form.board_12th,
                "start_date_12th": application_form.start_date_12th,
                "end_date_12th": application_form.end_date_12th,
                "percentage_12th": application_form.percentage_12th,
                "marks_12th": application_form.marks_12th,
                "username": registration.email,
                "status": exam_result.status,
                "company": exam_result.company,
                "marks": exam_result.marks,
                "department": exam_result.department,
            }
        }
        return render(request, "previewpage.html", context)

    except Exception as e:
        return JsonResponse({"success": False, "message": f"Error: {str(e)}"})

def update_password(user_email):
    # Fetch the user record (replace `Registration` with your actual user model)
    try:
        user = Registration.objects.get(email=user_email)
    except Registration.DoesNotExist:
        print(f"No user found with email: {user_email}")
        return False

    # Generate a new password
    new_password = generate_password(user.firstname)

    # Update the password in the database
    user.password = new_password
    user.save()

    # Send the new password to the user's email
    try:
        send_mail(
            subject="Your New Exam Credentials",
            message=(
                f"Dear {user.name},\n\n"
                f"We have received your payment for the re-exam. Your new credentials are as follows:\n\n"
                f"Username: {user.email}\n"
                f"Password: {new_password}\n\n"
                f"Please log in to take the exam.\n\n"
                f"Thank you."
            ),
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user_email],
            fail_silently=False,
        )
        print(f"Password update email sent to {user_email}.")
        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        return False
    
def handle_reexam_payment(request, email):
    try:
        user = get_object_or_404(ApplicationForm, email=email)
        new_password = generate_new_password(user.name)
        print(new_password)
        user.password = new_password
        user.save()

        send_mail(
            subject="Re-Exam Credentials",
            message=(
                f"Dear {user.name},\n\n"
                f"Your payment for the re-exam has been received. Your new login credentials are:\n\n"
                f"Username: {user.email}\n"
                f"Password: {new_password}\n\n"
                f"Please log in using this link: https://yourwebsite.com/exam-login\n\n"
                f"Thank you."
            ),
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[email],
            fail_silently=False,
        )
        return JsonResponse({"success": True, "message": "Re-exam credentials sent successfully."})
    except Exception as e:
        print(f"Error: {e}")
        return JsonResponse({"success": False, "message": "An error occurred."})

