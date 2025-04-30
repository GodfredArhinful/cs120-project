from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Patient, Consultation

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        if commit:
            user.save()
        return user

class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ['name', 'age', 'sex', 'phone_number', 'emergency_contact', 
                 'chief_complaint', 'medical_history', 'medications', 'allergies']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter patient\'s full name'
            }),
            'age': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter age'
            }),
            'sex': forms.Select(attrs={
                'class': 'form-select'
            }, choices=[('', 'Select sex'), ('M', 'Male'), ('F', 'Female')]),
            'phone_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter phone number'
            }),
            'emergency_contact': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter emergency contact details'
            }),
            'chief_complaint': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Enter chief complaint'
            }),
            'medical_history': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Enter medical history'
            }),
            'medications': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Enter current medications'
            }),
            'allergies': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Enter allergies'
            })
        }

class ConsultationForm(forms.ModelForm):
    class Meta:
        model = Consultation
        fields = ['patient', 'consultation_type', 'reason', 'diagnosis', 
                 'treatment_plan', 'tpa_administered', 'status']
        widgets = {
            'patient': forms.Select(attrs={
                'class': 'form-select'
            }),
            'consultation_type': forms.Select(attrs={
                'class': 'form-select'
            }),
            'reason': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Enter reason for consultation'
            }),
            'diagnosis': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Enter diagnosis'
            }),
            'treatment_plan': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Enter treatment plan'
            }),
            'tpa_administered': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'status': forms.Select(attrs={
                'class': 'form-select'
            })
        } 