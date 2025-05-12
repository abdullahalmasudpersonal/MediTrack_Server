from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import User
from .serializers import UserSerializer
from rest_framework import status
from django.db import transaction
from apps.patients.serializers import PatientSerializer
from apps.patients.utils import generate_user_id

# Create your views here.
@api_view(['GET'])
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
            # Step 1: Extract patient info
            # patient_data = {
            #     'name': request.data.get('name'),
            # }
            
            patient_serializer = PatientSerializer(data={**request.data,'userId': generate_user_id()})
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

# @api_view(['POST'])
# def createDoctor(request):
#     try:
#         with transaction.atomic():
    
#     except Exception as e:
#         return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)














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