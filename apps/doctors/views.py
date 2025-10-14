from rest_framework.response import Response
from rest_framework import status
from .models import Doctor
from .serializers import DoctorSerializer
from rest_framework.decorators import api_view
from apps.core.middleware.customAuthGird import custom_auth_gird
from apps.utils.response_helper import success_response, error_response

# Create your views here.
@api_view(['GET'])
def getAllDoctor(request):
   try:
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
      doctors = Doctor.objects.filter(user__status='active',user__is_deleted=False) 
      serializer = DoctorSerializer(doctors, many=True)
      return success_response(
         message="Get all doctor successfully",
         data=serializer.data, 
         code=status.HTTP_200_OK
         )  
   except Exception as e:
        return error_response(
            message="Failed get all doctor.",
            error=str(e),
            code=status.HTTP_400_BAD_REQUEST              
        )       

@api_view(['GET'])
def getSingleDoctor(request,pk):
     doctors = Doctor.objects.get(user_id=pk,user__status='active',user__is_deleted=False)
     serializer = DoctorSerializer(doctors)
     return Response(serializer.data, status=status.HTTP_200_OK)

