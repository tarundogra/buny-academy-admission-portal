from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.conf import settings
from .forms import StudentForm
from .models import Student
import random


def admission(request):
    if request.method == 'POST':
        form = StudentForm(request.POST, request.FILES)

        if form.is_valid():
            student = form.save()

            otp = str(random.randint(100000, 999999))

            request.session['otp'] = otp
            request.session['student_id'] = student.id
            request.session.modified = True

            try:
                send_mail(
                    subject='Your OTP Code',
                    message=f'Your OTP is: {otp}',
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[student.email],
                    fail_silently=False,
                    timeout=5,
                )
                print("EMAIL SENT SUCCESS")

            except Exception as e:
                print("EMAIL ERROR:", str(e))
                return render(request, 'students/admission.html', {
                    'form': form,
                    'error': 'Email could not be sent. Please check email settings.'
                })

            return redirect('verify_otp')

    else:
        form = StudentForm()

    return render(request, 'students/admission.html', {
        'form': form
    })


def verify_otp(request):
    if request.method == 'POST':
        user_otp = request.POST.get('otp')
        real_otp = request.session.get('otp')
        student_id = request.session.get('student_id')

        if str(user_otp) == str(real_otp):
            student = Student.objects.get(id=student_id)

            request.session.pop('otp', None)
            request.session.pop('student_id', None)

            return render(request, 'students/success.html', {
                'student': student
            })

        return render(request, 'students/verify_otp.html', {
            'error': 'Invalid OTP'
        })

    return render(request, 'students/verify_otp.html')