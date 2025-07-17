from rest_framework import serializers
from .models import Doctor
from apps.users.serializers import UserSerializer

class DoctorSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model = Doctor
        fields = ['id','user','name','phone_number','gender', 'birthDate','specialization','license_number','education','experience_years','hospital_affiliation','availability','consultation_type','fees','photo','bio','address','updated_at']
        
        read_only_fields = ['id', 'user']
        