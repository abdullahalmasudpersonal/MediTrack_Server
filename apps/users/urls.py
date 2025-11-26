from django.urls import path
from . import views

urlpatterns = [
    # path('ping/',views.pinkAllDoctor),
    path('<int:pk>/',views.singleUser),
    path('create_admin/',views.createAdmin), 
    path('create_doctor/',views.createDoctor), 
    path('create_patient/',views.createPatient), 
    path('my-profile-data/', views.getMyProfileData),
    path('update-profile-data/', views.updateMyProfileData),
    path('all-user/', views.getAllUser),
]