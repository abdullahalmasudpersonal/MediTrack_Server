from rest_framework import serializers
from .models import User
class UserSerializer(serializers.ModelSerializer):
   
    class Meta:
        model = User
        # fields = '__all__'
        fields = ['id', 'userId', 'email', 'password', 'role', 'status', 'last_login', 'created_at']
        extra_kwargs = {
            'password': {'write_only': True}
        }
        read_only_fields = ['id', 'userId', 'created_at']
        
    # def get_admin_profile(self, obj):
    #     if obj.role == 'admin' and hasattr(obj, 'admin_profile'):
    #         from apps.admins.serializers import AdminSerializer
    #         return AdminSerializer(obj.admin_profile).data
    #     return None

    # def get_doctor_profile(self, obj):
    #     if obj.role == 'doctor' and hasattr(obj, 'doctor_profile'):
    #         from apps.doctors.serializers import DoctorSerializer
    #         return DoctorSerializer(obj.doctor_profile).data
    #     return None

    # def get_patient_profile(self, obj):
    #     if obj.role == 'patient' and hasattr(obj, 'patient_profile'):
    #         from apps.patients.serializers import PatientSerializer
    #         return PatientSerializer(obj.patient_profile).data
    #     return None    
        
    # def get_admin_profile(self, obj):
    #     from apps.admins.serializers import AdminSerializer
    #     if hasattr(obj, 'admin_profile'):
    #         return AdminSerializer(obj.admin_profile).data
    #     return None

    # def get_doctor_profile(self, obj):
    #     from apps.doctors.serializers import DoctorSerializer
    #     if hasattr(obj, 'doctor_profile'):
    #         return DoctorSerializer(obj.doctor_profile).data
    #     return None

    # def get_patient_profile(self, obj):
    #     from apps.patients.serializers import PatientSerializer
    #     if hasattr(obj, 'patient_profile'):
    #         return PatientSerializer(obj.patient_profile).data
    #     return None