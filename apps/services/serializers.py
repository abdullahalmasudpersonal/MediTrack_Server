from rest_framework import serializers
from .models import Service
class ServiceSerializer(serializers.ModelSerializer):
   
    class Meta:
        model = Service
        # fields = ['id', 'name','category','short_description','description','description2','image', 'created_at']
        fields = '__all__'
        read_only_fields = ['id', 'created_at']