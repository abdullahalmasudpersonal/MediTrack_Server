from django.urls import path,include

urlpatterns = [
    path('user/',include('apps.users.urls')),
    path('doctor/', include('apps.doctors.urls')),
    path('appointment/', include('apps.appointments.urls')),
]