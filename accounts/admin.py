# accounts/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import UserProfile, Worker, PatientProfile, VitalSigns

class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False

class UserAdmin(BaseUserAdmin):
    inlines = (UserProfileInline,)

admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(UserProfile)

@admin.register(Worker)
class WorkerAdmin(admin.ModelAdmin):
    list_display = ('user', 'mobile_number', 'role')
    search_fields = ('user__username', 'mobile_number', 'role')
    list_filter = ('role',)

class PatientProfileAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'matriculation_number', 'email', 'mobile_no', 'birthday', 'marital_status', 'sex', 'blood_group', 'genotype', 'address', 'patient_height', 'mothers_number', 'fathers_number', 'image')
    search_fields = ('first_name', 'last_name', 'matriculation_number', 'email')
    list_filter = ('sex', 'blood_group', 'genotype', 'marital_status')
    ordering = ('last_name', 'first_name')

admin.site.register(PatientProfile, PatientProfileAdmin)

@admin.register(VitalSigns)
class VitalSignsAdmin(admin.ModelAdmin):
    list_display = ('patient', 'doctor', 'weight', 'blood_pressure', 'temperature', 'pulse', 'created_at')
    search_fields = ('patient__first_name', 'patient__last_name', 'doctor__user__username')
    list_filter = ('created_at', 'doctor', 'patient')