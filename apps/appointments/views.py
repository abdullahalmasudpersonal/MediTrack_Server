# from django.shortcuts import render
# from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
from apps.doctors.models import Doctor
# from apps.users.models import User
import uuid
from .models import Appointment
from .serializers import AppointmentSerializer
from apps.core.middleware.customAuthGird import custom_auth_gird
from datetime import datetime
from apps.schedules.models import Schedule
from apps.utils.response_helper import success_response, error_response

@api_view(['POST'])
@custom_auth_gird(allowed_roles=['admin','doctor','patient'],optional=True)
def create_appointment(request):
    try:
        data = request.data.copy()
        doctor_id = data.get('doctor')
        appointment_date_str = data.get('appointment_date')
        start_time_str = data.get('appointment_start_time')
        end_time_str = data.get('appointment_end_time')
        
        # 🔹 Doctor check
        doctor = Doctor.objects.filter(id=doctor_id).first()
        if not doctor:
            return error_response(
                message="Doctor not found.",
                error="Invalid doctor ID.",
                code=status.HTTP_404_NOT_FOUND
            )
        
        # 🔹 তারিখ ও সময় ঠিক আছে কিনা
        if not (appointment_date_str and start_time_str and end_time_str):
            return error_response(
                message="Date and time fields are required.",
                error="Missing required time/date fields.",
                code=status.HTTP_400_BAD_REQUEST
            )
        
        appointment_date = datetime.strptime(appointment_date_str, "%Y-%m-%d").date()
        start_time = datetime.strptime(start_time_str, "%H:%M").time()
        end_time = datetime.strptime(end_time_str, "%H:%M").time()

          # 🔹 ১️⃣ ডাক্তার ওই দিনে schedule আছে কিনা
        weekday = appointment_date.weekday()
        schedule = Schedule.objects.filter(doctor=doctor, weekday=weekday, is_active=True).first()
        if not schedule:
            return error_response(
                message="Doctor has no active schedule for this date.",
                error=f"No active schedule found for weekday {weekday}.",
                code=status.HTTP_400_BAD_REQUEST
            )
        
         # 🔹 ২️⃣ টাইম schedule এর মধ্যে কিনা যাচাই করো
        if not (schedule.start_time <= start_time and end_time <= schedule.end_time):
            return error_response(
                message="Appointment time is outside the doctor's schedule.",
                error="Invalid time slot.",
                code=status.HTTP_400_BAD_REQUEST
            )
        
        # 🔹 ৩️⃣ ওই সময় slot বুকড কিনা চেক করো
        overlapping = Appointment.objects.filter(
            doctor=doctor,
            appointment_date=appointment_date,
            appointment_start_time__lt=end_time,
            appointment_end_time__gt=start_time
        ).exists()

        if overlapping:
            return error_response(
                message="This time slot is already booked.",
                error="Time overlap detected.",
                code=status.HTTP_409_CONFLICT
            )
        
        # 🔹 Doctor এবং appointment নম্বর সেট করো
        data['doctor'] = doctor.id
        data['appointment_number'] = f"APT-{uuid.uuid4().hex[:10].upper()}"
        
        # 🔹 ইউজারের রোল চেক করে সম্পর্কিত ফিল্ড সেট করো
        user = getattr(request, 'user', None)
        if user and hasattr(user, 'id'):
            role = getattr(user, 'role', None)
            profile_id = getattr(user, 'profile_id', None)
            
            if role == 'patient' and profile_id:
                data['patient'] = profile_id
            elif role in ['doctor', 'admin']:
                data['created_by'] = user.id
        
        # 🔹 Appointment তৈরি
        serializer = AppointmentSerializer(data=data)  
        if serializer.is_valid():
            serializer.save()  
            return success_response(
                message="Appointment created successfully!",
                data=serializer.data,
                code=status.HTTP_201_CREATED
            )
        
        return error_response(
            message="Invalid appointment data.",
            error=serializer.errors,
            code=status.HTTP_400_BAD_REQUEST
        )

    except Exception as e:
        return error_response(
            message="Failed to create appointment.",
            error=str(e),
            code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

    
@api_view(['GET'])
@custom_auth_gird(allowed_roles=['patient','doctor', 'admin'])
def getAllAppointment(request):
    role = request.user.role
    email = request.user.email

    try:
        if role == 'patient':
            appointment = Appointment.objects.filter(email=email)
        elif role == 'doctor':
            appointment = Appointment.objects.filter(email=email)  
        elif role == 'admin':
            appointment = Appointment.objects.all()  
        else:
            return error_response(message="Your No Appointment", error=str(e), code=500)

        # If no appointments found
        if not appointment.exists():
            return error_response(message="No appointments found", code=404)
        
        # Serialize the appointments
        serializer = AppointmentSerializer(appointment, many=True)

        return success_response(
            message="Available slots fetched successfully",
            data=serializer.data,
            code=200
        )
    except Exception as e:
        return error_response(message="Failed to fetch appointment", error=str(e), code=500)


# @api_view(['GET'])
# @custom_auth_gird(allowed_roles=['admin'])
# def getAllappointment(request):
#     try:
#         appointments = Appointment.objects.all().order_by('-created_at')
#         serializer = AppointmentSerializer(appointments, many=True)
#         return Response( serializer.data, status=status.HTTP_200_OK)
#     except Exception as e:
#         return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

# @api_view(['GET'])
# @custom_auth_gird(allowed_roles=['admin'])
# def getSingleAppointment(request,pk):
    try:
        appointment = Appointment.objects.get(id=pk)
        serializer = AppointmentSerializer(appointment)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Appointment.DoesNotExist:
        return Response({'error': 'Appointment not found'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)