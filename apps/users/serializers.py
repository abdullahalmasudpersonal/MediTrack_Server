from rest_framework import serializers
from .models import User
# from apps.admins.serializers import AdminSerializer
# from apps.doctors.serializers import DoctorSerializer
# from apps.patients.serializers import PatientSerializer

class UserSerializer(serializers.ModelSerializer):
    # Admin to view all user profile data
    # admin_profile = AdminSerializer(read_only=True)
    # doctor_profile = DoctorSerializer(read_only=True)
    # patient_profile = PatientSerializer(read_only=True)
    admin_profile = serializers.SerializerMethodField()
    doctor_profile = serializers.SerializerMethodField()
    patient_profile = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = ['id', 'userId', 'email', 'password', 'role', 'status', 'last_login', 'created_at',  'admin_profile', 'doctor_profile', 'patient_profile']
        extra_kwargs = {
            'password': {'write_only': True}
        }
        read_only_fields = ['id', 'userId', 'created_at']
        
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