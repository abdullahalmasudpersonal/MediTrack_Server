from django.urls import path
from . import views

urlpatterns = [
    path('',views.allUser),
    path('<int:pk>/',views.singleUser),
    path('create_patient/',views.createPatient), 
    path('create_doctor/',views.createDoctor), 
]