from django.urls import path
from . import views
urlpatterns = [
       path('all-doctor/', views.getAllDoctor, name='get-all-doctors'),
]