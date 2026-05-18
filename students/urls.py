from django.urls import path
from . import views

urlpatterns = [

    path('', views.admission, name='admission'),

    path('verify/', views.verify_otp, name='verify_otp'),

]