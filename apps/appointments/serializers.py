from rest_framework import serializers
from apps.users.serializers import UserSerializer
from .models import Appointment
class AppointmentSerializer(serializers.ModelSerializer):
    # created_by = UserSerializer()
    # updated_by = UserSerializer()  
    
    class Meta:
        model = Appointment
        fields = '__all__'
        read_only_fields = ['id',  'created_at']
        