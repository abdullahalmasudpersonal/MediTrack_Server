
from rest_framework import serializers
from apps.users.models import User

class UserLimitedSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'role']
