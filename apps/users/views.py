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
from apps.core.middleware.decorators import role_required
import jwt
from django.conf import settings

# Create your views here.
# @login_required
# @role_required('admin', 'doctor','patient')
@api_view(['GET'])
def allUser(request):
    
    # print("see request result",request.META.get('HTTP_AUTHORIZATION'))
    token = request.headers.get('Authorization')
    if not token:
        return Response({'detail': 'Authorization header missing'}, status=status.HTTP_401_UNAUTHORIZED)
    
    try:
        decoded = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        existEmail = decoded.get('email')
        user = User.objects.get(email=existEmail)
        if user.role != 'admin':
         return Response({'detail': 'You are not authorized to view this data.'}, status=status.HTTP_403_FORBIDDEN)
     
        users = User.objects.filter(is_deleted=False)
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)
    
    except jwt.ExpiredSignatureError:
        return Response({'detail': 'Token has expired'}, status=status.HTTP_401_UNAUTHORIZED)
    except jwt.InvalidTokenError:
        return Response({'detail': 'Invalid token'}, status=status.HTTP_401_UNAUTHORIZED)
    except Exception as e:
        return Response({'detail': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

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
            # Step 1: Extract patient info
            # patient_data = {
            #     'name': request.data.get('name'),
            # }
            
            patient_serializer = PatientSerializer(data={**request.data,'userId': generate_patient_id()})
            # patient_serializer = PatientSerializer(data=patient_data)
            patient_serializer.is_valid(raise_exception=True)
            patient_serializer.save()
            
            # Step 2: Create user entry
            user_data = {
                'userId': patient_serializer.data["userId"],
                'email': patient_serializer.data['email'],
                'password': request.data.get('password'),
                'role': 'patient',
            }
            
            user_serializer = UserSerializer(data=user_data)
            user_serializer.is_valid(raise_exception=True)
            user_serializer.save()
            
            return Response({
            'patient': patient_serializer.data,
            'user': user_serializer.data
            }, status=status.HTTP_201_CREATED)

    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def createDoctor(request):
    try:
        with transaction.atomic():
            doctor_serializer = DoctorSerializer(data={**request.data,'userId':generate_doctor_id()})
            doctor_serializer.is_valid(raise_exception=True)
            doctor_serializer.save()
            
            user_data = {
                'userId':doctor_serializer.data['userId'],
                'email':doctor_serializer.data['email'],
                'password': request.data.get('password'),
                'role': 'doctor',
            }
            
            user_serializer = UserSerializer(data=user_data)
            user_serializer.is_valid(raise_exception=True)
            user_serializer.save()
            
            return Response({
            'doctor': doctor_serializer.data,
            'user': user_serializer.data
            }, status=status.HTTP_201_CREATED)
    
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def createAdmin(request):
    try:
        with transaction.atomic():
            admin_serializer = AdminSerializer(data={**request.data,'userId':generate_admin_id()})
            admin_serializer.is_valid(raise_exception=True)
            admin_serializer.save()
            
        user_data = {
            'userId':admin_serializer.data['userId'],
            'email':admin_serializer.data['email'],
            'password': request.data.get('password'),
            'role': 'admin',
            }   

        user_serializer = UserSerializer(data=user_data)
        user_serializer.is_valid(raise_exception=True)
        user_serializer.save()
        
        return Response({
        'admin': admin_serializer.data,
        'user': user_serializer.data
        }, status=status.HTTP_201_CREATED)    
    
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

# @role_required('ADMIN', 'SELLER', 'BUYER', 'SUPER_ADMIN')
# @api_view(['GET'])
# def getMyProfile(request):
#     users = User.objects.filter(is_deleted=False)










# def allUser(request):
#     # complex data
#     usr = User.objects.all()
#     # python dist 
#     serializer= UserSerializer(usr, many=True)
#     # Render Json 
#     json_data = JSONRenderer().render(serializer.data)
#     # json send to user
#     return HttpResponse(json_data, content_type="application/json")

# model instance
# def singleUser(request,pk):
#     # complex data
#     usr = User.objects.get(id=pk)
#     # python dist 
#     serializer= UserSerializer(usr)
#     # Render Json 
#     json_data = JSONRenderer().render(serializer.data)
#     # json send to user
#     return HttpResponse(json_data, content_type="application/json")


# from django.shortcuts import render
# def users(request):
#     course= " the Course is free"
#     module = 21
#     roll = "A-445 11"
#     offring = {"what":"lots of free offring", "c":course,"m":module,"r":roll}
#     techers = {"name":["tanvir", "masud","hasib","musa"]}
#     context = {**offring, **techers}
#     return render(request,"users.html", context=context)
    #  return HttpResponse("Welcome to MediTrack users ")

# def user(request):
#     return HttpResponse("Welcome to MediTrack Backend user"),