from django.shortcuts import render
from rest_framework.decorators import api_view
from .serializers import ScheduleSerializer
from rest_framework.response import Response
from rest_framework import status
from apps.doctors.models import Doctor
from .models import Schedule
from apps.utils.response_helper import success_response, error_response
from apps.appointments.models import Appointment
from datetime import datetime, timedelta

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
def getDoctorSchedule(request,pk):
    # try:
    #     # ⬇️ date ধরো query params থেকে
    #     date_str = request.GET.get("date")
    #     print(date_str,'date')
    #     if not date_str:
    #         return error_response(message="Date parameter is required.", code=400)

    #     # ⬇️ স্ট্রিং থেকে Date অবজেক্ট বানাও
    #     date = datetime.strptime(date_str, "%Y-%m-%d").date()

    #     # weekday বের করো (Monday=0, Tuesday=1 ...)
    #     weekday = date.weekday()
    #     print(weekday,'weekday')

    #     # doctor এর schedule বের করো
    #     schedule = Schedule.objects.filter(doctor_id=pk, weekday=weekday, is_active=True).first()
    #     print(schedule,'schedule')

    #     if not schedule:
    #         return error_response(message="No schedule found for this date.", code=404)

    #     # booked স্লট বের করো
    #     booked_slots = Appointment.objects.filter(
    #         doctor_id=pk,
    #         date=date
    #     ).values_list("start_time", "end_time")

    #     # এখন schedule অনুযায়ী slot বানাবে...
    #     # ... তারপর রেসপন্সে date ফেরত দেবে
    #     slots = [
    #         {"start_time": "09:00", "end_time": "09:30", "is_booked": False},
    #         {"start_time": "09:30", "end_time": "10:00", "is_booked": True},
    #     ]

    #     return success_response(
    #         message="Available slots fetched successfully",
    #         data={
    #             "doctor": {
    #                 "id": str(schedule.doctor.id),
    #                 "name": schedule.doctor.name,
    #                 "speciality": schedule.doctor.speciality,
    #             },
    #             "date": str(date),
    #             "weekday": date.strftime("%A"),  # Tuesday ইত্যাদি
    #             "slots": slots
    #         },
    #         code=200
    #     )

    # except Exception as e:
    #     return error_response(message="Failed to fetch slots", error=str(e), code=500)
    
    # try:
    #     doctor_id = pk

    #     if not doctor_id:
    #         return error_response(
    #             message="Doctor ID is required.",
    #             error="Missing doctor query parameter.",
    #             code=status.HTTP_400_BAD_REQUEST
    #         )

    #     schedules = Schedule.objects.filter(doctor_id=doctor_id).select_related('doctor')

    #     if not schedules.exists():
    #         return error_response(
    #             message="No schedules found for this doctor.",
    #             error=f"Doctor ID: {doctor_id}",
    #             code=status.HTTP_404_NOT_FOUND
    #         )

    #     serializer = ScheduleSerializer(schedules, many=True)

    #     return success_response(
    #         message="Doctor schedule fetched successfully.",
    #         data=serializer.data,
    #         code=status.HTTP_200_OK
    #     )

    # except Exception as e:
    #     return error_response(
    #         message="Failed to fetch doctor schedule.",
    #         error=str(e),
    #         code=status.HTTP_500_INTERNAL_SERVER_ERROR
    #     )


    try:
        date_str = request.GET.get("date")  # যেমন: 2025-10-30
        if not date_str:
            return error_response(message="Date parameter is required", code=400)
        
        date = datetime.strptime(date_str, "%Y-%m-%d").date()
        weekday = date.weekday()

        schedule = Schedule.objects.filter(
            doctor_id=pk,
            weekday=weekday,
            is_active=True
        ).first()

        if not schedule:
            return error_response(message="No active schedule found for this date", code=404)

        # বুকড স্লট বের করো (Booking model থেকে)
        booked_slots = Appointment.objects.filter(
            doctor_id=pk,
            appointment_date=date
        ).values_list('appointment_start_time', 'appointment_end_time')

        # Runtime slot generate
        appointment_start_time = datetime.combine(date, schedule.start_time)
        appointment_end_time = datetime.combine(date, schedule.end_time)
        delta = timedelta(minutes=schedule.slot_duration)

        start_time = appointment_start_time
        slots = []
        while start_time < appointment_end_time:
            slot_end = start_time + delta
            is_booked = any(
                (b_start <= start_time.time() < b_end) or (b_start < slot_end.time() <= b_end)
                for b_start, b_end in booked_slots
            )
            slots.append({
                "start_time": start_time.strftime("%H:%M"),
                "end_time": slot_end.strftime("%H:%M"),
                "is_booked": is_booked
            })
            start_time = slot_end

        return success_response(
            message="Available slots fetched successfully",
            data={
                "doctor": str(schedule.doctor.id),
                "date": str(date),
                "weekday": date.strftime("%A"),
                "slots": slots
            },
            code=200
        )

    except Exception as e:
        return error_response(message="Failed to fetch slots", error=str(e), code=500)





