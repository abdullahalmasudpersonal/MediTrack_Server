from django.urls import path
from . import views
urlpatterns = [
       path('all-doctor/', views.getAllDoctor, name='get-all-doctor'),
       path('all-doctor-admin/', views.getAllDoctorForAdmin, name='get-all-doctor-admin'),
       path('single-doctor/<str:pk>/', views.getSingleDoctor, name='get-single-doctors'),
       path('update-doctor-status/<str:pk>/', views.updateDoctorStatus, name='update-doctor-status'),
]