from django.shortcuts import render, redirect
from django.core.mail import send_mail, EmailMessage
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

            # SAVE STUDENT + FILES PROPERLY
            student = form.save(commit=False)
            student.save()

            # GENERATE OTP
            otp = str(random.randint(100000, 999999))
            request.session['otp'] = otp

            # STORE ID FOR LATER
            request.session['student_id'] = student.id

            # SEND OTP EMAIL TO STUDENT
            try:
                send_mail(
                    'Buny Academy OTP Verification',
                    f'Your OTP is: {otp}',
                    'bunyacademy@gmail.com',
                    [student.email],
                    fail_silently=False,
                )
            except Exception as e:
                print("OTP EMAIL ERROR:", e)

            return redirect('verify_otp')

    else:
        form = StudentForm()

    return render(request, 'students/admission.html', {'form': form})


# =========================
# OTP VERIFY VIEW
# =========================
def verify_otp(request):

    if request.method == 'POST':

        user_otp = request.POST.get('otp')
        real_otp = request.session.get('otp')

        if str(user_otp) == str(real_otp):

            student_id = request.session.get('student_id')
            student = Student.objects.get(id=student_id)

            # =========================
            # OWNER EMAIL WITH FILES
            # =========================
            try:

                message = f"""
NEW ADMISSION RECEIVED

Name: {student.name}
Phone: {student.phone}
Email: {student.email}
Address: {student.address}

Exam: {student.exam}
Training Type: {student.training_type}

BPL: {student.bpl}
IRDP: {student.irdp}
Widow: {student.widow}

Physical Training: {student.physical_training}
Undertaking: {student.undertaking}
"""

                email = EmailMessage(
                    'New Admission - Buny Academy',
                    message,
                    'bunyacademy@gmail.com',
                    ['bunyacademy@gmail.com']   # 👈 change this
                )

                # =========================
                # ATTACH DOCUMENTS
                # =========================
                if student.aadhaar:
                    email.attach_file(student.aadhaar.path)

                if student.marksheet:
                    email.attach_file(student.marksheet.path)

                if student.photo:
                    email.attach_file(student.photo.path)

                if student.signature:
                    email.attach_file(student.signature.path)

                email.send(fail_silently=False)

            except Exception as e:
                print("ADMIN EMAIL ERROR:", e)

            return render(request, 'students/success.html', {
                'student': student
            })

        else:
            return render(request, 'students/verify_otp.html', {
                'error': 'Invalid OTP'
            })

    return render(request, 'students/verify_otp.html')