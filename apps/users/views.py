from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
def users(request):
    course= " The Course is free"
    module = 21
    roll = "A-445"
    
    offring = {"what":"lots of free offring", "c":course,"m":module,"r":roll}
    return render(request,"users.html", context=offring)
    #  return HttpResponse("Welcome to MediTrack users ")

# def user(request):
#     return HttpResponse("Welcome to MediTrack Backend user"),