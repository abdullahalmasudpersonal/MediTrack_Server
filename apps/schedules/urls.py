from django.urls import path
from . import views

urlpatterns = [
       path('create-schedule/', views.createSchedule, name='create-schedule'),
       path('get-doctor-schedules/<str:pk>/', views.getDoctorSchedule, name='get-doctor-schedules')
]