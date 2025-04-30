
from django.shortcuts import render
from django.http import HttpResponse
from . models import User
from . serializers import UserSerializer
from rest_framework.renderers import JSONRenderer

# Create your views here.
def allUser(request):
    # complex data
    usr = User.objects.all()
    # python dist 
    serializer= UserSerializer(usr, many=True)
    # Render Json 
    json_data = JSONRenderer().render(serializer.data)
    # json send to user
    return HttpResponse(json_data, content_type="application/json")

# model instance
def singleUser(request,pk):
    # complex data
    usr = User.objects.get(id=pk)
    # python dist 
    serializer= UserSerializer(usr)
    # Render Json 
    json_data = JSONRenderer().render(serializer.data)
    # json send to user
    return HttpResponse(json_data, content_type="application/json")



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