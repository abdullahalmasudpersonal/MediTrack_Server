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
        #  'user__status': 'active',
        #  'user__is_deleted': False,
      }
      if specialization:
         filters['specialization__icontains'] = specialization

      if name:
         filters['name__icontains'] = name 
      
      doctors = Doctor.objects.filter(**filters)  
    #   doctors = Doctor.objects.filter(user__status='active',user__is_deleted=False) 
    #   doctors = Doctor.objects.filter() 
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
    try:
        doctors = Doctor.objects.get(user_id=pk,user__status='active',user__is_deleted=False)
        serializer = DoctorSerializer(doctors)
        return success_response(
            message="Single doctor fetched successfully",
            data=serializer.data,
            code=status.HTTP_200_OK
        )
    except Doctor.DoesNotExist:
        return error_response(
            message="Doctor not found.",
            error="No doctor exists with this ID.",
            code=status.HTTP_404_NOT_FOUND
        ) 
    except Exception as e:   
        return error_response(
            message="Failed to fetch single doctor.",
            error=str(e),
            code=status.HTTP_400_BAD_REQUEST
        )
    
@api_view(['PATCH'])
@custom_auth_gird(allowed_roles=['admin'])
def updateDoctorStatus(request,pk):
    print(request.data.get,'request'),
    try:
        doctor = Doctor.objects.get(user_id=pk)
        new_status = request.data.get('status')

        if not new_status:
            return error_response(
                message="Status field is required.",
                error="Missing 'status' in request data.",
                code=status.HTTP_400_BAD_REQUEST
            )

        # স্ট্যাটাস আপডেট করা
        doctor.user.status = new_status
        doctor.user.save()

        return success_response(
            message="Doctor status updated successfully",
            data={"user_id": pk, "status": new_status},
            code=status.HTTP_200_OK
        )

    except Doctor.DoesNotExist:
        return error_response(
            message="Doctor not found.",
            error="Invalid doctor ID.",
            code=status.HTTP_404_NOT_FOUND
        )
    
    except Exception as e:
        return error_response(
            message="Failed to update doctor status.",
            error=str(e),
            code=status.HTTP_400_BAD_REQUEST
        )

    


