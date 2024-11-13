# accounts/models.py
from django.db import models
from django.contrib.auth.models import User    
from django.utils import timezone

class UserProfile(models.Model):
    USER_ROLES = (
        ('nurse', 'Nurse'),
        ('doctor', 'Doctor'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email = models.EmailField(max_length=30)
    role = models.CharField(max_length=20, choices=USER_ROLES)
    phone_number = models.CharField(max_length=15)
    profile_picture = models.ImageField(upload_to='profile_pictures', blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    birthday = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.user.username
    
class Worker(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    mobile_number = models.CharField(max_length=15, unique=True)
    biography = models.TextField(null=True, blank=True)
    role = models.CharField(max_length=50)

    def __str__(self):
        return self.user.username
    

class PatientProfile(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    matriculation_number = models.CharField(max_length=20, unique=True)
    email = models.EmailField()
    mobile_no = models.CharField(max_length=11)
    birthday = models.DateField()
    marital_status = models.CharField(max_length=20, choices=[('Married', 'Married'), ('Unmarried', 'Unmarried')])
    sex = models.CharField(max_length=10, choices=[('Male', 'Male'), ('Female', 'Female')])
    blood_group = models.CharField(max_length=5, choices=[('A+', 'A+'), ('A-', 'A-'), ('B+', 'B+'), ('B-', 'B-'), ('O+', 'O+'), ('O-', 'O-'), ('AB+', 'AB+'), ('AB-', 'AB-')])
    genotype = models.CharField(max_length=2, choices=[('AA', 'AA'), ('AS', 'AS'), ('AC', 'AC'), ('SS', 'SS'), ('SC', 'SC')])
    address = models.TextField()
    patient_height = models.CharField(max_length=10)
    image = models.ImageField(upload_to='patients/', blank=True, null=True)
    mothers_number = models.CharField(max_length=11)
    fathers_number = models.CharField(max_length=11)
    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class VitalSigns(models.Model):
    patient = models.ForeignKey(PatientProfile, on_delete=models.CASCADE)
    doctor = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    weight = models.CharField(max_length=10)
    blood_pressure = models.CharField(max_length=10)
    temperature = models.CharField(max_length=10)
    pulse = models.CharField(max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)  # This field will store the time when the vital sign was created
    status = models.CharField(max_length=20, default='Not Started')  # Add this field

class Prescription(models.Model):
    doctor = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    patient = models.ForeignKey(PatientProfile, on_delete=models.CASCADE, related_name='prescriptions')  # Define related_name here
    symptoms = models.TextField()
    diagnosis = models.TextField()
    treatment = models.TextField()
    drugs = models.JSONField()  # [{'drug': 'Drug1', 'dosage': 'Dosage1'}, ...]
    tests = models.JSONField(blank=True, null=True)  # ['Test1', 'Test2', ...]
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    treatment_given = models.BooleanField(default=False)  # New field
    prescription_given = models.BooleanField(default=False)

    def __str__(self):
        return f'Prescription for {self.patient} by {self.doctor}'

class Message(models.Model):
    sender = models.ForeignKey(Worker, related_name='sent_messages', on_delete=models.CASCADE)
    recipient = models.ForeignKey(Worker, related_name='received_messages', on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)
    
    def __str__(self):
        return f"From {self.sender} to {self.recipient} at {self.timestamp}"


class MedicalHistory(models.Model):
    patient = models.ForeignKey('PatientProfile', related_name='medical_histories', on_delete=models.CASCADE)
    date = models.DateField(default=timezone.now)
    doctor = models.CharField(UserProfile, max_length=100)
    symptoms = models.TextField()
    diagnosis = models.TextField()
    treatment = models.TextField()
    drugs = models.JSONField(blank=True, null=True)  # Store drugs as JSON
    tests = models.TextField(blank=True)  # Store tests as comma-separated string

    def __str__(self):
        return f"{self.date} - {self.doctor}"
