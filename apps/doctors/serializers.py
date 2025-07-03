from rest_framework import serializers
from .models import Doctor
from apps.users.serializers import UserSerializer

class DoctorSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model = Doctor
        fields = '__all__'
        read_only_fields = ['id', 'user']