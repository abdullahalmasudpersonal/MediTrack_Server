from rest_framework.decorators import api_view
from .models import Patient
from rest_framework.response import Response
from rest_framework import status
from .serializers import PatientSerializer

# Create your views here.
@api_view(['POST'])
def createPatient(request):
    serializer = PatientSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)
