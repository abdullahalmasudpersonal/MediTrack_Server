from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        extra_kwargs = {
            'password': {'write_only': True}
        }

    # def create(self, validated_data):
    #     user = User(**validated_data)
    #     user.save()
    #     return user







# class UserSerializer(serializers.Serializer):
#     STATUS_CHOICES = [
#         ('active', 'Active'),
#         ('inactive', 'Inactive'),
#     ]
    
#     ROLE_CHOICES = [
#         ('admin','Admin'),
#         ('doctor','Doctor'),
#         ('patient','Patient')
#     ]
    
#     userId = serializers.CharField(max_length=10)
#     email = serializers.CharField(max_length=30)  
#     password = serializers.CharField(max_length=128)
#     role = serializers.ChoiceField( choices=ROLE_CHOICES,default='patient')
#     status = serializers.ChoiceField( choices=STATUS_CHOICES, default='active')
#     created_at = serializers.DateTimeField(read_only=True)
#     updated_at = serializers.DateTimeField(read_only=True)
#     is_deleted = serializers.BooleanField(default=False)