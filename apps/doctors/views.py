from rest_framework.response import Response
from rest_framework import status
from .models import Doctor
from .serializers import DoctorSerializer
from rest_framework.decorators import api_view
from apps.core.middleware.customAuthGird import custom_auth_gird

# Create your views here.
@api_view(['GET'])
def getAllDoctor(request):
     specialization  = request.GET.get('specialization')
     name = request.GET.get('name')
     filters = {
        'user__status': 'active',
        'user__is_deleted': False,
    }
     if specialization:
        filters['specialization__icontains'] = specialization

     if name:
        filters['name__icontains'] = name 
        
     doctors = Doctor.objects.filter(**filters)   
     # doctors = Doctor.objects.filter(user__status='active',user__is_deleted=False)
     serializer = DoctorSerializer(doctors, many=True)
     return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def getSingleDoctor(request,pk):
     doctors = Doctor.objects.get(user_id=pk,user__status='active',user__is_deleted=False)
     serializer = DoctorSerializer(doctors)
     return Response(serializer.data, status=status.HTTP_200_OK)

