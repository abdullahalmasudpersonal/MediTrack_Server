from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import User
from .serializers import UserSerializer
from rest_framework import status
from django.db import transaction
from apps.admins.serializers import AdminSerializer
from apps.doctors.serializers import DoctorSerializer
from apps.patients.serializers import PatientSerializer
from apps.admins.utils import generate_admin_id
from apps.doctors.utils import generate_doctor_id
from apps.patients.utils import generate_patient_id
from apps.core.middleware.customAuthGird import custom_auth_gird
from apps.doctors.models import Doctor
from apps.admins.models import Admin
from apps.patients.models import Patient
from apps.utils.response_helper import success_response, error_response
import cloudinary
import cloudinary.uploader

# @api_view(['GET'])
# def pinkAllDoctor(request):
#     users = Doctor.objects.filter()
#     serializer = DoctorSerializer(users, many=True)
#     return Response(serializer.data)

# Create your views here.
@api_view(['GET'])
@custom_auth_gird(allowed_roles=['admin'])
# def custom_auth_gird(allowed_roles=None):  # ✅ Best Practice
# def custom_auth_gird(allowed_roles=[]):  # ❌ এটা কখনো করো না!
def allUser(request):
    users = User.objects.filter(is_deleted=False)
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def singleUser(request, pk):
    try:
        user = User.objects.get(pk=pk, is_deleted=False)
    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
    serializer = UserSerializer(user)
    return Response(serializer.data)

@api_view(['POST'])
def createPatient(request):
    try:
       with transaction.atomic(): 
            user_data ={
                'email': request.data.get('email'),
                'password': request.data.get('password'),
                'role': 'patient',
            }
            
            user_serializer = UserSerializer(data=user_data)
            user_serializer.is_valid(raise_exception=True)
            user = user_serializer.save()
            user.userId = generate_patient_id()
            user.save()
            
            patient_data = {
                'name': request.data.get('name'),
                'age': request.data.get('age'),
                'birthDate': request.data.get('birthDate'),
                'patient_photo': request.data.get('patient_photo',None),
                'phone_number': request.data.get('phone_number'),
                'address': request.data.get('address'),
            }
            
            patient_serializer = PatientSerializer(data=patient_data)
            patient_serializer.is_valid(raise_exception=True)
            patient_serializer.save(user=user)
            
            return Response({
            "patient": patient_serializer.data
        }, status=status.HTTP_201_CREATED)
            
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)  

@api_view(['POST'])
@custom_auth_gird(allowed_roles=['admin'])
def createDoctor(request):
    try:
        with transaction.atomic():
            user_data ={
                'email': request.data.get('email'),
                'password': request.data.get('password'),
                'role': 'doctor',
            }
            
            user_serializer = UserSerializer(data=user_data)
            user_serializer.is_valid(raise_exception=True)
            user = user_serializer.save()
            user.userId = generate_doctor_id()
            user.save()
            
            doctor_data = {
                'name': request.data.get('name'),
                'phone_number': request.data.get('phone_number'),
                'gender':request.data.get('gender'),
                'birthDate':request.data.get('birthDate'),
                'specialization':request.data.get('specialization'),
                'license_number':request.data.get('license_number'),
                'education':request.data.get('education'),
                'experience_years':request.data.get('experience_years'),
                'hospital_affiliation':request.data.get('hospital_affiliation'),
                'availability':request.data.get('availability'),
                'fees':request.data.get('fees'),
                'doctor_photo':request.data.get('doctor_photo'),
                'bio':request.data.get('bio'),
                'address': request.data.get('address'),
            }
            
            doctor_serializer = DoctorSerializer(data=doctor_data)
            doctor_serializer.is_valid(raise_exception=True)
            doctor_serializer.save(user=user)
            
        return success_response(
            message="Doctor created successfully",
            data=doctor_serializer.data,
            code=status.HTTP_201_CREATED
        )
            
    except Exception as e:
        return error_response(
            message="Doctor creation failed",
            error=str(e),
            code=status.HTTP_400_BAD_REQUEST              
        )   
            
@api_view(['POST'])
@custom_auth_gird(allowed_roles=['admin'])
def createAdmin(request):
    try:
        with transaction.atomic():
            user_data ={
                'email': request.data.get('email'),
                'password': request.data.get('password'),
                'role': 'admin',
            }
            user_serializer = UserSerializer(data=user_data)
            user_serializer.is_valid(raise_exception=True)
            user = user_serializer.save()
            user.userId = generate_admin_id()
            user.save()
            
            admin_data = {
                'name': request.data.get('name'),
                'phone_number': request.data.get('phone_number'),
                'address': request.data.get('address'),
                'admin_photo': request.data.get('admin_photo',None),
            }
            
            admin_serializer = AdminSerializer(data=admin_data)
            admin_serializer.is_valid(raise_exception=True)
            admin_serializer.save(user=user)
        
        return Response({
            "admin": admin_serializer.data
        }, status=status.HTTP_201_CREATED)
            
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)    

@api_view(['GET'])
@custom_auth_gird(allowed_roles=['admin','doctor','patient'])
def getMyProfileData(request):
    role = request.user.role
    email = request.user.email
    
    profile = None
    serializer = None
    
    try:
        if role == 'admin':
            profile = Admin.objects.get(user=request.user)
            serializer = AdminSerializer(profile)
        elif role == 'doctor':
            profile = Doctor.objects.get(user=request.user)
            serializer = DoctorSerializer(profile)
        elif role == 'patient':
            profile = Patient.objects.get(user=request.user)
            serializer = PatientSerializer(profile)
        else:
            return Response({'detail': 'Unsupported role'}, status=status.HTTP_400_BAD_REQUEST)    
                
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    except (Admin.DoesNotExist, Doctor.DoesNotExist, Patient.DoesNotExist):
        return Response({'detail': 'Profile not found'}, status=status.HTTP_404_NOT_FOUND)
    
    except Exception as e:
        return Response({'detail': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)    

@api_view(['PATCH'])
@custom_auth_gird(allowed_roles=['admin','doctor','patient'])
def updateMyProfileData(request):
    role = request.user.role
    email = request.user.email
    
    try:
        if role == 'admin':
            profile = Admin.objects.get(user=request.user)
            # serializer = AdminSerializer(profile, data=request.data, partial=True)
            serializer_class = AdminSerializer

        elif role == 'doctor':
            profile = Doctor.objects.get(user=request.user)
            # serializer = DoctorSerializer(profile, data=request.data, partial=True)
            serializer_class = DoctorSerializer
            
        elif role == 'patient':
            profile = Patient.objects.get(user=request.user)
            # serializer = PatientSerializer(profile, data=request.data, partial=True)
            serializer_class = PatientSerializer
            
        else:
            return Response({'detail': 'Invalid role'}, status=400)
        
        data = request.data.copy()
        print(data,'data')
        # if "image" in request.FILES:
        #     upload_result = cloudinary.uploader.upload(request.FILES["image"])
        #     data["image"] = upload_result.get("secure_url")  # শুধু URL save হবে

        serializer = serializer_class(profile, data=data, partial=True)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=400)
            
    except Exception as e:
        return Response({'detail': str(e)}, status=500)    

@api_view(['GET'])
@custom_auth_gird(allowed_roles=['admin'])
def getAllUser(request):
    users = User.objects.all()
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

