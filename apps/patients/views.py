from rest_framework.decorators import api_view
from .models import Patient
from rest_framework.response import Response
from rest_framework import status
from .serializers import PatientSerializer
from apps.core.middleware.customAuthGird import custom_auth_gird

# Create your views here.
@api_view(['GET'])
@custom_auth_gird(allowed_roles=['admin'])
def getAllPatient(request):
    doctors = Patient.objects.all()
    serializer = PatientSerializer(doctors, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
# @custom_auth_gird(allowed_roles=['admin'])
def getSinglePatient(request,pk):
    doctors = Patient.objects.filter(user_id=pk)
    serializer = PatientSerializer(doctors, many=True)
    print(pk,'doctors',serializer.data)
    return Response(serializer.data, status=status.HTTP_200_OK)
    # return Response('HTTP_200_OK')