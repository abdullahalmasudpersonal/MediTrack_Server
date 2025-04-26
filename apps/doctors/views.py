from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def doctors(request):
     return HttpResponse("Welcome to MediTrack doctors")