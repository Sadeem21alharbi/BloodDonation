from django.urls import path
from . import views

app_name = 'hospital' 

urlpatterns = [
    path('login/', views.hospital_login, name='hospital_login'),
    path('register/', views.hospital_register, name='hospital_register'),
    path('logout/', views.hospital_logout, name='hospital_logout'),

    path('dashboard/', views.hospital_dashboard, name='dashboard'),
    path('dashboard/profile/', views.hospital_profile, name='profile'),
    path('dashboard/profile/update/', views.hospital_profile_update, name='profile_update'),
    
    path('dashboard/requests/', views.donation_requests, name='requests'),
    path('dashboard/requests/create/', views.request_create, name='request_create'),
    
    path('dashboard/responses/', views.donor_responses, name='responses'),
    
    path('dashboard/analytics/', views.analytics, name='analytics'),
    
    path('dashboard/settings/', views.hospital_settings, name='settings'),
]
