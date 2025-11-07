from django.urls import path
from . import views
urlpatterns = [
    path('create-appointment/',views.create_appointment ),
    path('all-appointment/',views.getAllAppointment ),
    # path('single-appointment/<str:pk>/',views.getSingleAppointment ),
]