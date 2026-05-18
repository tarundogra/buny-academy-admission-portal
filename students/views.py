from django.shortcuts import render, redirect
from django.core.mail import send_mail
from .forms import StudentForm
from .models import Student
import random


def admission(request):

    if request.method == 'POST':

        form = StudentForm(request.POST, request.FILES)

        if form.is_valid():

            # GENERATE OTP
            otp = random.randint(100000, 999999)

            # SAVE OTP
            request.session['otp'] = otp

            # SAVE FORM DATA IN SESSION
            request.session['name'] = request.POST.get('name')
            request.session['phone'] = request.POST.get('phone')
            request.session['email'] = request.POST.get('email')
            request.session['address'] = request.POST.get('address')
            request.session['exam'] = request.POST.get('exam')
            request.session['training_type'] = request.POST.get('training_type')

            # CHECKBOX DATA
            request.session['is_bpl'] = 'is_bpl' in request.POST
            request.session['is_irdp'] = 'is_irdp' in request.POST
            request.session['is_widow'] = 'is_widow' in request.POST
            request.session['physical_training'] = 'physical_training' in request.POST
            request.session['undertaking'] = 'undertaking' in request.POST

            # SEND OTP EMAIL
            try:

                send_mail(
                    'Buny Academy OTP Verification',
                    f'Your OTP is: {otp}',
                    'bunyacademy@gmail.com',
                    [request.POST.get('email')],
                    fail_silently=False,
                )

            except Exception as e:
                print("EMAIL ERROR:", e)

            return redirect('verify_otp')

    else:
        form = StudentForm()

    return render(request, 'admission.html', {'form': form})


def verify_otp(request):

    if request.method == 'POST':

        user_otp = request.POST.get('otp')

        # VERIFY OTP
        if str(user_otp) == str(request.session.get('otp')):

            # SAVE STUDENT
            student = Student.objects.create(

                name=request.session.get('name'),
                phone=request.session.get('phone'),
                email=request.session.get('email'),
                address=request.session.get('address'),

                exam=request.session.get('exam'),
                training_type=request.session.get('training_type'),

                is_bpl=request.session.get('is_bpl'),
                is_irdp=request.session.get('is_irdp'),
                is_widow=request.session.get('is_widow'),

                physical_training=request.session.get('physical_training'),
                undertaking=request.session.get('undertaking'),
            )

            # SEND ADMIN MAIL
            try:

                message = f"""
New Admission Received

Name: {student.name}
Phone: {student.phone}
Email: {student.email}

Address: {student.address}

Exam: {student.exam}
Training Type: {student.training_type}

BPL: {student.is_bpl}
IRDP: {student.is_irdp}
Widow: {student.is_widow}

Physical Training: {student.physical_training}
Undertaking Accepted: {student.undertaking}
"""

                send_mail(
                    'New Admission - Buny Academy',
                    message,
                    'bunyacademy@gmail.com',
                    ['bunyacademy@gmail.com'],
                    fail_silently=True,
                )

            except Exception as e:
                print("ADMIN EMAIL ERROR:", e)

            return render(request, 'success.html', {
                'student': student
            })

        else:

            return render(request, 'verify_otp.html', {
                'error': 'Invalid OTP'
            })

    return render(request, 'verify_otp.html')