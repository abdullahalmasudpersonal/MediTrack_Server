from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
from apps.doctors.models import Doctor
from apps.users.models import User
import uuid
from .models import Appointment
from .serializers import AppointmentSerializer
from apps.core.middleware.customAuthGird import custom_auth_gird

@api_view(['POST'])
@custom_auth_gird(allowed_roles=['admin','doctor','patient'],optional=True)
def create_appointment(request):
    try:
        data = request.data.copy()
        doctor_id = data.get('doctor')
        
        try:
            doctor = Doctor.objects.get(id=doctor_id)
        except Doctor.DoesNotExist:
            return Response({'error': 'Doctor not found.'}, status=status.HTTP_404_NOT_FOUND)
        
        data['doctor'] = doctor.id
        data['appointment_number'] = f"APT-{uuid.uuid4().hex[:10].upper()}"
        
        user = request.user
        
        if user:
            role = user.role
            profile_id = user.profile_id
            
            if role == 'patient' and profile_id:
                data['patient'] = profile_id
                print('user',profile_id,user.id)
            elif role in ['doctor', 'admin']:
                data['created_by'] = user.id
        
        serializer = AppointmentSerializer(data=data)  
        if serializer.is_valid():
            serializer.save()  
            return Response({'message': 'Appointment created successfully!', 'data': serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e: return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)  
    
@api_view(['GET'])
@custom_auth_gird(allowed_roles=['admin'])
def getAllappointment(request):
    try:
        appointments = Appointment.objects.all().order_by('-created_at')
        serializer = AppointmentSerializer(appointments, many=True)
        return Response( serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@custom_auth_gird(allowed_roles=['admin'])
def getSingleAppointment(request,pk):
    try:
        appointment = Appointment.objects.get(id=pk)
        serializer = AppointmentSerializer(appointment)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Appointment.DoesNotExist:
        return Response({'error': 'Appointment not found'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)