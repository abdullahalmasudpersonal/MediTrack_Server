from django.urls import path
from . import views

urlpatterns = [
    path('',views.allUser),
    path('ping/',views.pinkAllDoctor),
    path('<int:pk>/',views.singleUser),
    path('create_admin/',views.createAdmin), 
    path('create_doctor/',views.createDoctor), 
    path('create_patient/',views.createPatient), 
]