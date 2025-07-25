from django.urls import path
from . import views

urlpatterns = [
    path('create-service/',views.createService),
    path('all-service/',views.getAllService),
    path('single-service/<str:pk>/',views.getSingleService),
]