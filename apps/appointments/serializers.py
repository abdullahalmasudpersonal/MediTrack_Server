from rest_framework import serializers
from apps.users.serializers import UserSerializer
from .models import Appointment
class AppointmentSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)
    updated_by = UserSerializer(read_only=True)  
    
    class Meta:
        model = Appointment
        fields = '__all__'
        read_only_fields = ['id', 'appointment_number', 'created_by', 'updated_by', 'created_at']
        