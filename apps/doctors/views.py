from rest_framework.response import Response
from rest_framework import status
from .models import Doctor
from .serializers import DoctorSerializer
from rest_framework.decorators import api_view
from apps.core.middleware.customAuthGird import custom_auth_gird

# Create your views here.
@api_view(['GET'])
# @custom_auth_gird(allowed_roles=['admin'])
def getAllDoctor(request):
     doctors = Doctor.objects.all()
     serializer = DoctorSerializer(doctors, many=True)
     return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
# @custom_auth_gird(allowed_roles=['admin'])
def getSingleDoctor(request,pk):
     doctors = Doctor.objects.filter(user_id=pk)
     serializer = DoctorSerializer(doctors, many=True)
     return Response(serializer.data, status=status.HTTP_200_OK)

