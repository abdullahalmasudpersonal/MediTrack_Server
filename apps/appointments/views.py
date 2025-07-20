from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
from apps.users.models import User
import uuid
from .models import Appointment
from .serializers import AppointmentSerializer

@api_view(['POST'])
def create_appointment(request):
    try:
        data = request.data.copy()
        doctor_id = data.get('doctor')
        try:
            doctor = User.objects.get(id=doctor_id)
            if doctor.role != 'doctor':
                return Response({'error': 'User is not a doctor.'}, status=status.HTTP_400_BAD_REQUEST)
            if doctor.status != 'active':
                return Response({'error': 'Doctor is not active.'}, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response({'error': 'Doctor not found.'}, status=status.HTTP_404_NOT_FOUND)
        
        data['doctor'] = doctor.id
        data['appointment_number'] = f"APT-{uuid.uuid4().hex[:10].upper()}"
        if request.user.is_authenticated:
            data['created_by'] = request.user.id
            data['updated_by'] = request.user.id
        
        serializer = AppointmentSerializer(data=data)  
        if serializer.is_valid():
            serializer.save()  
            return Response({'message': 'Appointment created successfully!', 'data': serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e: return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)  
    
    
    