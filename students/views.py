from django.shortcuts import render, redirect
from django.core.mail import send_mail, EmailMessage
from django.conf import settings
from .forms import StudentForm
from .models import Student
import random


# =========================
# ADMISSION VIEW
# =========================
def admission(request):

    if request.method == 'POST':

        form = StudentForm(request.POST, request.FILES)

        if form.is_valid():

            # SAVE STUDENT
            student = form.save()

            # GENERATE OTP
            otp = str(random.randint(100000, 999999))

            # SAVE OTP IN SESSION
            request.session['otp'] = otp
            request.session['student_id'] = student.id

            # GET EMAIL
            email = student.email

            # SEND OTP EMAIL
            try:

                send_mail(
                    subject='Your OTP Code',
                    message=f'Your OTP is: {otp}',
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[email],
                    fail_silently=False,
                )

                print("EMAIL SENT SUCCESS")

            except Exception as e:

                print("EMAIL ERROR:", str(e))

            return redirect('verify_otp')

        else:

            print(form.errors)

    else:

        form = StudentForm()

    return render(request, 'students/admission.html', {
        'form': form
    })


# =========================
# VERIFY OTP VIEW
# =========================
def verify_otp(request):

    if request.method == 'POST':

        user_otp = request.POST.get('otp')
        real_otp = request.session.get('otp')

        # CHECK OTP
        if str(user_otp) == str(real_otp):

            student_id = request.session.get('student_id')

            try:
                student = Student.objects.get(id=student_id)

            except Student.DoesNotExist:

                return render(request, 'students/verify_otp.html', {
                    'error': 'Student not found'
                })

            # SEND DETAILS TO ADMIN
            try:

                message = f"""
NEW ADMISSION RECEIVED

Name: {student.name}
Phone: {student.phone}
Email: {student.email}
Address: {student.address}

Exam: {student.exam}
Training Type: {student.training_type}
"""

                admin_email = EmailMessage(
                    subject='New Admission - Buny Academy',
                    body=message,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    to=['bunyacademy@gmail.com']
                )

                # ATTACH FILES
                if student.aadhaar:
                    admin_email.attach_file(student.aadhaar.path)

                if student.marksheet:
                    admin_email.attach_file(student.marksheet.path)

                if student.photo:
                    admin_email.attach_file(student.photo.path)

                if student.signature:
                    admin_email.attach_file(student.signature.path)

                admin_email.send(fail_silently=False)

                print("ADMIN EMAIL SENT")

            except Exception as e:

                print("ADMIN EMAIL ERROR:", str(e))

            return render(request, 'students/success.html', {
                'student': student
            })

        else:

            return render(request, 'students/verify_otp.html', {
                'error': 'Invalid OTP'
            })

    return render(request, 'students/verify_otp.html')