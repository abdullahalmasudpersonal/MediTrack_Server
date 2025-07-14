from django.urls import path
from . import views

urlpatterns = [
    path('all-patient/',views.getAllPatient),
    path('single-patient/<str:pk>/',views.getSinglePatient),
    # path('create/',views.createPatient), 
]