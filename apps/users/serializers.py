
from rest_framework import serializers
class UserSerializer(serializers.Serializer):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
    ]
    
    ROLE_CHOICES = [
        ('admin','Admin'),
        ('doctor','Doctor'),
        ('patient','Patient')
    ]
    
    userId = serializers.CharField(max_length=10)
    email = serializers.CharField(max_length=30)  
    password = serializers.CharField(max_length=128)
    role = serializers.ChoiceField( choices=ROLE_CHOICES,default='patient')
    status = serializers.ChoiceField( choices=STATUS_CHOICES, default='active')
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)
    is_deleted = serializers.BooleanField(default=False)