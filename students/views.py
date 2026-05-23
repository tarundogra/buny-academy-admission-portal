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

            request.session['otp'] = otp
            request.session['student_id'] = student.id

            # SEND OTP EMAIL
            try:
                send_mail(
                    'OTP Verification',
                    f'Your OTP is {otp}',
                    settings.DEFAULT_FROM_EMAIL,
                    [student.email],
                    fail_silently=False,
                )

                print("EMAIL SENT SUCCESS")

            except Exception as e:
                print("EMAIL ERROR:", str(e))

            return redirect('verify_otp')

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

        if str(user_otp) == str(real_otp):

            student_id = request.session.get('student_id')
            student = Student.objects.get(id=student_id)

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

                email = EmailMessage(
                    'New Admission - Buny Academy',
                    message,
                    settings.DEFAULT_FROM_EMAIL,
                    ['bunyacademy@gmail.com']
                )

                # ATTACH FILES
                if student.aadhaar:
                    email.attach_file(student.aadhaar.path)

                if student.marksheet:
                    email.attach_file(student.marksheet.path)

                if student.photo:
                    email.attach_file(student.photo.path)

                if student.signature:
                    email.attach_file(student.signature.path)

                email.send(fail_silently=False)

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