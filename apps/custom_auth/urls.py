from django.urls import path
from . import views

urlpatterns = [
    #  path('',views.allUser),
     path('login/', views.login_view, name='login'),
     path('change-password/', views.change_password,)
]
