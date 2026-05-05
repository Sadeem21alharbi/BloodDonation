from django.urls import path
from . import views

app_name = 'hospital'

urlpatterns = [

    # Authentication
    path('login/', views.hospital_login, name='hospital_login'),
    path('register/', views.hospital_register, name='hospital_register'),
    path('logout/', views.hospital_logout, name='hospital_logout'),
    
    # Dashboard
   path('dashboard/', views.hospital_dashboard, name='dashboard'),
   
   # Profile management
    path('profile/', views.hospital_profile, name='profile'),

    path(
        'profile/update/',
        views.hospital_profile_update,
        name='profile_update'
    ),
   
   # Donation request management
   path('requests/', views.donation_requests, name='requests'),
   path('requests/create/', views.donation_request_create, name='request_create'),
   path('requests/<int:request_id>/details/', views.donation_request_detail, name='request_detail'),
   path('requests/<int:request_id>/update/', views.update_donation_request, name='request_update'),
   path('requests/<int:request_id>/delete/', views.delete_donation_request, name='request_delete'),
   

   
   # Donor responses
   
    path('responses/',views.donor_responses, name='responses'),
    path('responses/<int:response_id>/',views.donor_response_details,name='donor_response_details'),
    path('responses/<int:response_id>/status/',views.update_response_status,name='update_response_status'),
    path('responses/<int:response_id>/delete/',views.delete_donor_response,name='delete_donor_response'),

    # Analytics
   path('analytics/', views.hospital_dashboard, name='analytics'),
   
   # Settings
   path('settings/', views.hospital_settings, name='settings'),
    
]