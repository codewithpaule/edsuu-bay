# views.py
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .models import UserProfile
from django.db import transaction
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import UserProfile, Worker, PatientProfile, VitalSigns, Prescription, MedicalHistory, Message
from django.shortcuts import render, get_object_or_404
from django.template.defaultfilters import slugify
from functools import wraps
from django.http import HttpResponseForbidden
from django.shortcuts import redirect
from django.db import IntegrityError
from django.contrib import messages
from datetime import datetime, timedelta

def role_required(role):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if request.user.is_authenticated:
                user_profile = UserProfile.objects.get(user=request.user)
                if user_profile.role == role:
                    return view_func(request, *args, **kwargs)
                else:
                    # Redirect to a custom error page (e.g., 404 page)
                    return redirect('error404')  # Update 'error404' with your actual URL name for the error page
            else:
                return redirect('login')
        return _wrapped_view
    return decorator

# Authentications
def forgot_password(request):
    return render(request, 'authentication/page-forgot-password.html')

def logout_view(request):
    logout(request)
    return redirect('login')  # Redirect to the login page after logout

def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        role = request.POST['role']
        phone_number = request.POST['phone_number']
        profile_picture = request.FILES.get('profile_picture')

        if User.objects.filter(username=username).exists():
            return render(request, 'authentication/page-register.html', {'error': 'Username already exists.'})

        try:
            with transaction.atomic():
                user = User.objects.create_user(
                    username=username,
                    email=email,
                    password=password,
                    first_name=first_name,
                    last_name=last_name
                )
                user_profile = UserProfile.objects.create(
                    user=user,
                    role=role,
                    phone_number=phone_number,
                    profile_picture=profile_picture
                )

                # Create a Worker instance if the role is a worker
                if role.lower() in ['doctor', 'nurse']:
                    Worker.objects.create(
                        user=user,
                        role=role,
                        mobile_number=phone_number,
                        biography='Short biography'  # Add appropriate biography
                    )
            return redirect('login')
        except Exception as e:
            return render(request, 'authentication/page-register.html', {'error': str(e)})
    return render(request, 'authentication/page-register.html')

def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return render(request, 'authentication/page-login.html', {'error': 'Invalid email or password.'})

        user = authenticate(request, username=user.username, password=password)
        
        if user is not None:
            auth_login(request, user)
            user_profile = UserProfile.objects.get(user=user)
            if user_profile.role == 'doctor':
                return redirect('homedoc')
            elif user_profile.role == 'nurse':
                return redirect('homenurse')
        else:
            return render(request, 'authentication/page-login.html', {'error': 'Invalid email or password.'})
    
    return render(request, 'authentication/page-login.html')

def error404(request):
    return render(request, 'authentication/page-error-404.html')

def custom_login(request):
    return render(request, 'authentication/page-error-404.html')

# Doctor Panel
@login_required(login_url='/custom_login/')
@role_required('doctor')
def homedoc(request):
    user_profile = UserProfile.objects.get(user=request.user)
    vital_signs = VitalSigns.objects.filter(doctor=user_profile).select_related('patient')
    context = {
        'user_profile': user_profile,
        'vital_signs': vital_signs,
    }
    return render(request, 'doctor/index.html', context)

@login_required(login_url='/custom_login/')
@role_required('doctor')
def prescription(request, patient_id):
    patient = get_object_or_404(PatientProfile, id=patient_id)
    vital_sign = VitalSigns.objects.filter(patient=patient).order_by('-created_at').first()

    if request.method == 'POST':
        symptoms = request.POST.get('symptoms')
        diagnosis = request.POST.get('diagnosis')
        treatment = request.POST.get('treatment')

        num_drugs = int(request.POST.get('numDrugs', 0))
        drugs = []
        for i in range(1, num_drugs + 1):
            drug = request.POST.get(f'drug{i}')
            dosage = request.POST.get(f'dosage{i}')
            if drug and dosage:
                drugs.append({'drug': drug, 'dosage': dosage})

        num_tests_str = request.POST.get('numTests', '')  # Get the value as string
        num_tests = int(num_tests_str) if num_tests_str.isdigit() else 0  # Convert to int if not empty and is a digit
        tests = []
        for i in range(1, num_tests + 1):
            test = request.POST.get(f'test{i}')
            if test:
                tests.append(test)

        Prescription.objects.create(
                doctor=request.user.userprofile,
                patient=patient,
                symptoms=symptoms,
                diagnosis=diagnosis,
                treatment=treatment,
                drugs=drugs,
                tests=tests,
                prescription_given=True,  # Set as given when created
        )

        # Create MedicalHistory instance
        MedicalHistory.objects.create(
            patient=patient,
            doctor=request.user.userprofile,
            symptoms=symptoms,
            diagnosis=diagnosis,
            treatment=treatment,
            drugs=drugs,
            tests=", ".join(tests) if tests else "",  # Convert tests list to comma-separated string
        )

        messages.success(request, 'Prescription created and sent to the nurse.')
        return redirect('homedoc')  # Redirect to doctor's home page

    return render(request, 'doctor/new-prescription.html', {'patient': patient, 'vital_sign': vital_sign})

@login_required(login_url='/custom_login/')
@role_required('doctor')
def appointment(request):
    return render(request, 'doctor/new-appointment.html')

@login_required(login_url='/custom_login/')
@role_required('doctor')
def all_prescriptions(request):
    return render(request, 'doctor/all-prescriptions.html')

@login_required(login_url='/custom_login/')
@role_required('doctor')
def all_patients(request):
    patients = PatientProfile.objects.all()
    return render(request, 'doctor/all-patients.html', {'patients': patients})

@login_required(login_url='/custom_login/')
@role_required('doctor')
def doc_inbox(request):
    recipient = Worker.objects.get(user=request.user)
    messages_received = Message.objects.filter(recipient=recipient).exclude(sender=recipient)
    return render(request, 'doctor/inbox-doctor.html', {'messages_received': messages_received})

@login_required(login_url='/custom_login/')
@role_required('doctor')
def view_message(request, message_id):
    # Retrieve the specific message based on its ID
    message = get_object_or_404(Message, id=message_id)

    # Retrieve the current user (recipient)
    recipient = Worker.objects.get(user=request.user)

    # Retrieve all messages received by the current user, excluding messages sent by the user
    messages_received = Message.objects.filter(recipient=recipient).exclude(sender=recipient)

    # Render the template with the message and other received messages
    return render(request, 'doctor/view-message.html', {'message': message, 'messages_received': messages_received})


@login_required(login_url='/custom_login/')
@role_required('doctor')
def messaged_viewed(request, message_id):
    message = get_object_or_404(Message, id=message_id)
    # Update the treatment_given attribute
    message.read = True
    message.save()
    # Redirect to the page where you want to display the updated status
    return redirect('doctorinbox')  # replace 'prescription_list' with your target view name


@login_required(login_url='/custom_login/')
@role_required('doctor')
def worker_profile(request, worker_id):
    worker = get_object_or_404(Worker, id=worker_id)
    
    if request.method == 'POST':
        content = request.POST.get('msg')
        if content:
            sender = Worker.objects.get(user=request.user)
            recipient = worker
            Message.objects.create(sender=sender, recipient=recipient, content=content)
            messages.success(request, 'Message sent successfully!')
            return redirect('doc_profile', worker_id=worker_id)
        else:
            messages.error(request, 'Please enter a message before sending.')

    return render(request, 'doctor/doctor-profile.html', {'worker': worker})

@login_required(login_url='/custom_login/')
@role_required('doctor')
def doc_settings(request):
    user = request.user
    user_profile = user.userprofile
    worker = Worker.objects.get(user=user)

    if request.method == 'POST':
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.email = request.POST.get('email')
        user.save()
        
        user_profile.phone_number = request.POST.get('phone_number')
        user_profile.birthday = request.POST.get('birthday')
        user_profile.address = request.POST.get('address')
        user_profile.bio = request.POST.get('bio')
        
        worker.biography = request.POST.get('bio')
        
        if request.FILES.get('profile_picture'):
            user_profile.profile_picture = request.FILES.get('profile_picture')
        
        user_profile.save()
        worker.save()
        
        return redirect('doctorsettings')
    
    context = {
        'user': user,
        'user_profile': user_profile,
        'worker': worker
    }
    return render(request, 'settings/doctor-settings.html', context)

@login_required(login_url='/custom_login/')
@role_required('doctor')
def workers_list(request):
    # Retrieve the current user's UserProfile
    current_user_profile = UserProfile.objects.get(user=request.user)

    # Filter out the current user from the queryset of workers
    workers = UserProfile.objects.filter(role__in=['doctor', 'nurse']).exclude(user=current_user_profile.user)

    return render(request, 'doctor/doctor-list.html', {'workers': workers})

@login_required(login_url='/custom_login/')
@role_required('doctor')
def patient_profile(request, patient_id):
    patient = get_object_or_404(PatientProfile, id=patient_id)
    medical_history = patient.medical_histories.all()
    prescriptions = patient.prescriptions.all()

    return render(request, 'doctor/patient-profile.html', {'patient': patient, 'medical_history': medical_history, 'prescriptions': prescriptions})

@login_required(login_url='/custom_login/')
@role_required('doctor')
def view_medical_history(request, history_id):
    history = get_object_or_404(MedicalHistory, id=history_id)
    return render(request, 'doctor/medical-history.html', {'history': history})

# Nurse Panel
@login_required(login_url='/custom_login/')
@role_required('nurse')
def homenurse(request):
    patients = PatientProfile.objects.all()
    doctors = UserProfile.objects.filter(role='doctor')
    vital_signs = VitalSigns.objects.select_related('doctor', 'patient').all()  # Include related doctor and patient
    return render(request, 'nurse/nurse.html', {
        'patients': patients,
        'doctors': doctors,
        'vital_signs': vital_signs
    })

@login_required(login_url='/custom_login/')
@role_required('nurse')
def post_to_doctor(request):
    if request.method == 'POST':
        patient_id = request.POST.get('patient')
        doctor_id = request.POST.get('doctor')
        weight = request.POST.get('weight')
        bloodpress = request.POST.get('bloodpress')
        temperature = request.POST.get('temperature')
        pulse = request.POST.get('pulse')

        try:
            patient = get_object_or_404(PatientProfile, id=patient_id)
            doctor = get_object_or_404(UserProfile, user__id=doctor_id, role='doctor')

            VitalSigns.objects.create(
                patient=patient,
                doctor=doctor,
                weight=weight,
                blood_pressure=bloodpress,
                temperature=temperature,
                pulse=pulse,
                status='Posted to Dr.'
            )
            messages.success(request, 'Vital signs posted to the doctor successfully.')
        except Exception as e:
            messages.error(request, f'An error occurred while posting vital signs: {e}')

        return redirect('vitals')
    else:
        return redirect('vitals')

 
@login_required(login_url='/custom_login/')
@role_required('nurse')
def get_vitals(request):
    if request.method == 'POST':
        patient_id = request.POST.get('patient')
        doctor_id = request.POST.get('doctor')
        weight = request.POST.get('weight')
        bloodpress = request.POST.get('bloodpress')
        temperature = request.POST.get('temperature')
        pulse = request.POST.get('pulse')

        try:
            patient = get_object_or_404(PatientProfile, id=patient_id)
            doctor = get_object_or_404(UserProfile, user__id=doctor_id, role='doctor')

            VitalSigns.objects.create(
                patient=patient,
                doctor=doctor,
                weight=weight,
                blood_pressure=bloodpress,
                temperature=temperature,
                pulse=pulse
            )
            
            messages.success(request, 'Vital signs posted to the doctor successfully.')
        except Exception as e:
            messages.error(request, f'An error occurred while posting vital signs: {e}')

        return redirect('homenurse')
    else:
        patients = PatientProfile.objects.all()
        doctors = UserProfile.objects.filter(role='doctor')
        return render(request, 'nurse/get-vitals.html', {'patients': patients, 'doctors': doctors})

@login_required(login_url='/custom_login/')
@role_required('nurse')
def all_patient_nurse(request):
    patients = PatientProfile.objects.all()
    doctors = UserProfile.objects.filter(role='doctor')
    return render(request, 'nurse/all-patients.html', {'patients': patients, 'doctors': doctors})

@login_required(login_url='/custom_login/')
@role_required('nurse')
def add_patient(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        matriculation_number = request.POST.get('matriculation_number')
        email = request.POST.get('email')
        mobile_no = request.POST.get('mobile_no')
        birthday = request.POST.get('birthday')
        marital_status = request.POST.get('marital_status')
        sex = request.POST.get('sex')
        blood_group = request.POST.get('blood_group')
        genotype = request.POST.get('genotype')
        address = request.POST.get('address')
        patient_height = request.POST.get('patient_height')
        mothers_number = request.POST.get('mothers_number')
        fathers_number = request.POST.get('fathers_number')
        image = request.FILES.get('image')

        try:
            patient_profile = PatientProfile(
                first_name=first_name,
                last_name=last_name,
                matriculation_number=matriculation_number,
                email=email,
                mobile_no=mobile_no,
                birthday=birthday,
                marital_status=marital_status,
                sex=sex,
                blood_group=blood_group,
                genotype=genotype,
                address=address,
                patient_height=patient_height,
                mothers_number=mothers_number,
                fathers_number=fathers_number,
                image=image
            )
            patient_profile.save()
            messages.success(request, 'Patient profile created successfully!')
        except IntegrityError:
            messages.error(request, 'A patient with this matriculation number already exists, enter fresh information.')
        
    return render(request, 'nurse/new-patient.html')

@login_required(login_url='/custom_login/')
@role_required('nurse')
def workers_list_nurse(request):
    # Retrieve the current user's UserProfile
    current_user_profile = UserProfile.objects.get(user=request.user)

    # Filter out the current user from the queryset of workers
    workers = UserProfile.objects.filter(role__in=['doctor', 'nurse']).exclude(user=current_user_profile.user)

    return render(request, 'nurse/worker-list.html', {'workers': workers})

@login_required(login_url='/custom_login/')
@role_required('nurse')
def workers_profile_nurse(request, worker_id):
    worker = get_object_or_404(Worker, id=worker_id)
    
    if request.method == 'POST':
        content = request.POST.get('msg')
        if content:
            sender = Worker.objects.get(user=request.user)
            recipient = worker
            Message.objects.create(sender=sender, recipient=recipient, content=content)
            messages.success(request, 'Message sent successfully!')
            return redirect('workerprofile', worker_id=worker_id)
        else:
            messages.error(request, 'Please enter a message before sending.')

    return render(request, 'nurse/worker-profile.html', {'worker': worker})


@login_required(login_url='/custom_login/')
@role_required('nurse')
def treatment(request):
    prescriptions = Prescription.objects.select_related('patient', 'doctor').all()
    return render(request, 'nurse/treatment.html', {'prescriptions': prescriptions})

@login_required(login_url='/custom_login/')
@role_required('nurse')
def view_treatment(request, prescription_id):
    prescription = get_object_or_404(Prescription, id=prescription_id)
    return render(request, 'nurse/view-treatment.html', {'prescription': prescription})

@login_required(login_url='/custom_login/')
@role_required('nurse')
def treatment_done(request, prescription_id):
    prescription = get_object_or_404(Prescription, id=prescription_id)
    # Update the treatment_given attribute
    prescription.treatment_given = True
    prescription.save()
    # Redirect to the page where you want to display the updated status
    return redirect('treatment')  # replace 'prescription_list' with your target view name


@login_required(login_url='/custom_login/')
@role_required('nurse')
def nurse_patientprof(request, patient_id):
    patient = get_object_or_404(PatientProfile, id=patient_id)
    medical_history = patient.medical_histories.all()
    prescriptions = patient.prescriptions.all()

    return render(request, 'nurse/patient-profile.html', {'patient': patient, 'medical_history': medical_history, 'prescriptions': prescriptions})


@login_required(login_url='/custom_login/')
@role_required('nurse')
def view_medical_history_nurse(request, history_id):
    history = get_object_or_404(MedicalHistory, id=history_id)
    return render(request, 'nurse/medical-history.html', {'history': history})



@login_required(login_url='/custom_login/')
@role_required('nurse')
def nurse_inbox(request):
    recipient = Worker.objects.get(user=request.user)
    messages_received = Message.objects.filter(recipient=recipient).exclude(sender=recipient)
    return render(request, 'nurse/inbox-nurse.html', {'messages_received': messages_received})

@login_required(login_url='/custom_login/')
@role_required('nurse')
def view_message_nurse(request, message_id):
    # Retrieve the specific message based on its ID
    message = get_object_or_404(Message, id=message_id)

    # Retrieve the current user (recipient)
    recipient = Worker.objects.get(user=request.user)

    # Retrieve all messages received by the current user, excluding messages sent by the user
    messages_received = Message.objects.filter(recipient=recipient).exclude(sender=recipient)

    # Render the template with the message and other received messages
    return render(request, 'nurse/view-message.html', {'message': message, 'messages_received': messages_received})


@login_required(login_url='/custom_login/')
@role_required('nurse')
def message_seen(request, message_id):
    message = get_object_or_404(Message, id=message_id)
    # Update the treatment_given attribute
    message.read = True
    message.save()
    # Redirect to the page where you want to display the updated status
    return redirect('nurse_inbox')  # replace 'prescription_list' with your target view name



@login_required(login_url='/custom_login/')
@role_required('nurse')
def nurse_settings(request):
    user = request.user
    user_profile = user.userprofile
    worker = Worker.objects.get(user=user)
    

    if request.method == 'POST':
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.email = request.POST.get('email')
        user.save()
        
        user_profile.phone_number = request.POST.get('phone_number')
        user_profile.birthday = request.POST.get('birthday')
        user_profile.address = request.POST.get('address')
        user_profile.bio = request.POST.get('bio')
        
        worker.biography = request.POST.get('bio')
        
        if request.FILES.get('profile_picture'):
            user_profile.profile_picture = request.FILES.get('profile_picture')
        
        user_profile.save()
        worker.save()
        
        return redirect('nurse_settings')
    
    context = {
        'user': user,
        'user_profile': user_profile,
        'worker': worker
    }
    return render(request, 'settings/nurse-settings.html', context)
