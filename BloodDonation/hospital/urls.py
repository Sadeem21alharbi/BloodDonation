from django.urls import path
from . import views

app_name = 'hospital' 

urlpatterns = [
    path('login/', views.hospital_login, name='login'),
    path('register/', views.hospital_register, name='register'),

    path('dashboard/', views.hospital_dashboard, name='dashboard'),
    path('dashboard/profile/', views.hospital_profile, name='profile'),
    path('dashboard/requests/', views.donation_requests, name='requests'),
    path('dashboard/responses/', views.donor_responses, name='responses'),
    path('dashboard/analytics/', views.analytics, name='analytics'),
    path('dashboard/settings/', views.settings, name='settings'),
]