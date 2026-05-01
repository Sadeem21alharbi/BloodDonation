from django.urls import path
from . import views

app_name = 'donor' 

urlpatterns = [
    path('dashboard/', views.donor_dashboard, name='donor_home'),
    path('login/', views.donor_login, name='login'),
    path('register/', views.donor_register, name='register'),
]

