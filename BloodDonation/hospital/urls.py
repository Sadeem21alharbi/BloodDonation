from django.urls import path
from . import views

app_name = 'hospital' 

urlpatterns = [
    path('login/', views.hospital_login, name='login'),
    path('register/', views.hospital_register, name='register'),
]