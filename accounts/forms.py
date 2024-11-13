# accounts/forms.py
from django import forms
from django.contrib.auth.models import User
from .models import UserProfile, Worker, PatientProfile

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['profile_picture', 'phone_number', 'address', 'bio', 'birthday']

class WorkerForm(forms.ModelForm):
    class Meta:
        model = Worker
        fields = ['role', 'mobile_number', 'biography']

class PatientsInfoForm(forms.ModelForm):
    class Meta:
        model = PatientProfile
        fields = '__all__'
        widgets = {
            'birthday': forms.DateInput(attrs={'type': 'date'}),
            'marital_status': forms.Select(choices=[('Married', 'Married'), ('Unmarried', 'Unmarried')]),
            'sex': forms.Select(choices=[('Male', 'Male'), ('Female', 'Female')]),
            'blood_group': forms.Select(choices=[('A+', 'A+'), ('A-', 'A-'), ('B+', 'B+'), ('B-', 'B-'), ('O+', 'O+'), ('O-', 'O-'), ('AB+', 'AB+'), ('AB-', 'AB-')]),
            'genotype': forms.Select(choices=[('AA', 'AA'), ('AS', 'AS'), ('AC', 'AC'), ('SS', 'SS'), ('SC', 'SC')]),
        }