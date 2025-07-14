from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework import status
from .models import Doctor
from .serializers import DoctorSerializer
from rest_framework.decorators import api_view

# Create your views here.
@api_view(['GET'])
def getAllDoctor(request):
     doctors = Doctor.objects.all()
     serializer = DoctorSerializer(doctors, many=True)
     # print(serializer.data,'data')
     return Response(serializer.data, status=status.HTTP_200_OK)
     # return HttpResponse("Welcome to MediTrack doctors")