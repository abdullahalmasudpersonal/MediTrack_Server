from django.urls import path
from . import views

urlpatterns = [
       path('create-schedule/', views.createSchedule, name='create-schedule'),
       path('get-doctor-schedules/<str:pk>/available-slots/', views.getDoctorSchedule, name='get-doctor-schedules')
]