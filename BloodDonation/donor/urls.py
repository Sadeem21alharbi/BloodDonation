from django.urls import path
from . import views

app_name = 'donor' 

urlpatterns = [
    path('login/', views.donor_login, name='login'),
    path('register/', views.donor_register, name='register'),
]