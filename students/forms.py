from django import forms
from .models import Student


class StudentForm(forms.ModelForm):

    class Meta:

        model = Student

        fields = '__all__'

        widgets = {

            'exam': forms.Select(attrs={

                'class': 'custom-select'

            })

        }