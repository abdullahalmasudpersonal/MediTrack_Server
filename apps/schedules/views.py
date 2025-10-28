from django.shortcuts import render
from rest_framework.decorators import api_view
from .serializers import ScheduleSerializer
from rest_framework.response import Response
from rest_framework import status
from apps.doctors.models import Doctor
from .models import Schedule
from apps.utils.response_helper import success_response, error_response

@api_view(['POST'])
def createSchedule(request):
    try:
    # serializer = ScheduleSerializer(data=request.data)
        data = request.data
        print(data,'data')
        doctor_id = data.get("doctor")
        if not doctor_id:
            return error_response(
                message="Doctor ID is required.",
                error="Missing field: doctor",
                code=status.HTTP_400_BAD_REQUEST
            )

        try:
            doctor = Doctor.objects.get(id=doctor_id)
        except Doctor.DoesNotExist:
            return error_response(
                message="Doctor not found.",
                error=f"No doctor found with id {doctor_id}",
                code=status.HTTP_404_NOT_FOUND
            )
    
        serializer = ScheduleSerializer(data=data)
        if serializer.is_valid():
            serializer.save(doctor=doctor)
            return success_response(
                message="Schedule created successfully.",
                data=serializer.data,
                code=status.HTTP_201_CREATED
            )
        else:
            return error_response(
                message="Invalid data provided.",
                error=serializer.errors,
                code=status.HTTP_400_BAD_REQUEST
            ) 

    except Exception as e:
        return error_response(
            message="Failed to create schedule.",
            error=str(e),
            code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['GET'])
def getDoctorSchedule(request):
    try:
        doctor_id = request.query_params.get("doctor")

        if not doctor_id:
            return error_response(
                message="Doctor ID is required.",
                error="Missing doctor query parameter.",
                code=status.HTTP_400_BAD_REQUEST
            )

        schedules = Schedule.objects.filter(doctor_id=doctor_id).select_related('doctor')

        if not schedules.exists():
            return error_response(
                message="No schedules found for this doctor.",
                error=f"Doctor ID: {doctor_id}",
                code=status.HTTP_404_NOT_FOUND
            )

        serializer = ScheduleSerializer(schedules, many=True)

        return success_response(
            message="Doctor schedule fetched successfully.",
            data=serializer.data,
            code=status.HTTP_200_OK
        )

    except Exception as e:
        return error_response(
            message="Failed to fetch doctor schedule.",
            error=str(e),
            code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )




