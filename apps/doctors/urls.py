from django.urls import path
from . import views
urlpatterns = [
       path('all-doctor/', views.getAllDoctor, name='get-all-doctors'),
       path('single-doctor/<str:pk>/', views.getSingleDoctor, name='get-single-doctors'),
]