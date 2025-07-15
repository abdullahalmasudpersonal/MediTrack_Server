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
    patient = Patient.objects.filter(user__status='active',user__is_deleted=False)
    serializer = PatientSerializer(patient, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
@custom_auth_gird(allowed_roles=['admin'])
def getSinglePatient(request,pk):
    patient = Patient.objects.get(user_id=pk,user__status='active',user__is_deleted=False)
    serializer = PatientSerializer(patient)
    return Response(serializer.data, status=status.HTTP_200_OK)