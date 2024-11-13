from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', login, name='login'),
    path('Forgot Password/', forgot_password, name='forgotpassword'),
    path('Register/', register, name='register'),
    path('error404/', error404, name='error404'),
    path('logout/', logout_view, name='logout'),
    path('custom_login/', custom_login, name='custom_login'),


    # Doctor Url
    path('doctor/', homedoc, name='homedoc'),
    path('doctor/prescription/<int:patient_id>', prescription, name='prescription'),
    path("doctor/worker-list", workers_list, name='doctors'),
    path("doctor/worker/<int:worker_id>", worker_profile, name='doc_profile'),    
    path("doctor/prescriptions", all_prescriptions, name='allprescription'),
    path("doctor/patients", all_patients, name='allpatients'),
    path("doctor/patient-profile/<int:patient_id>", patient_profile, name='patientprofile'),
    path('doctor/view-medical-history/<int:history_id>/', view_medical_history, name='view_medical_history'),
    path("doctor/inbox/", doc_inbox, name='doctorinbox'),
    path("doctor/view-message/<int:message_id>", view_message, name='viewmessage'),
    path("doctor/messaged_viewed/<int:message_id>", messaged_viewed, name='messaged_viewed'),
    path("doctor/account-settings/", doc_settings, name='doctorsettings'),

    
    # Nurse Url
    path('nurse/', homenurse, name='homenurse'),
    path('nurse/post-to-doctor', post_to_doctor, name='post_to_doctor'),
    path('nurse/patients', all_patient_nurse, name='all_patient_nurse'),
    path('nurse/vitals/', get_vitals, name='vitals'),
    path("nurse/inbox/", nurse_inbox, name='nurse_inbox'),
    path("nurse/message/<int:message_id>", view_message_nurse, name='view_message'),
    path("nurse/message-seen/<int:message_id>", message_seen, name='message_seen'),
    path("nurse/add-patient/", add_patient, name='add_patient_nurse'),
    path("nurse/worker-list/", workers_list_nurse, name='workers'),
    path("nurse/worker/<int:worker_id>", workers_profile_nurse, name='workerprofile'),
    path("nurse/patient-profile/<int:patient_id>", nurse_patientprof, name='patient_profile'),
    
    path('nurse/medical_history_nurse/<int:history_id>/', view_medical_history_nurse, name='view_medical_history_nurse'),
    path("nurse/account-settings/", nurse_settings, name='nurse_settings'),
    path("nurse/give-treatment/", treatment, name='treatment'),
    path('nurse/view-treatment/<int:prescription_id>/', view_treatment, name='view_treatment'),
    path('nurse/treatment_done/<int:prescription_id>/', treatment_done, name='treatment_done'),


    # Add other paths as needed
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
