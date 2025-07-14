from django.urls import path
from . import views
urlpatterns = [
    path('all-admin/', views.getAllAdmin, name='get-all-admin'),
    path('single-admin/<str:pk>/', views.getSingleAdmin, name='get-single-admin'),
]