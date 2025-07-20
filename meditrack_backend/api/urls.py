from django.urls import path,include

urlpatterns = [
    path('user/',include('apps.users.urls')),
    path('admin/', include('apps.admins.urls')),
    path('doctor/', include('apps.doctors.urls')),
    path('patient/', include('apps.patients.urls')),
    path('appointment/', include('apps.appointments.urls')),
    path('auth/', include('apps.custom_auth.urls')),
]