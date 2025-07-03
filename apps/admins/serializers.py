from rest_framework import serializers
from .models import Admin
from apps.users.serializers import UserSerializer

class AdminSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)    
    class Meta:
        model = Admin
        fields = '__all__'
        read_only_fields = ['id', 'user',]