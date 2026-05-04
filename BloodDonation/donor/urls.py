from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views

app_name = 'donor' 

urlpatterns = [
    path('dashboard/', views.donor_dashboard, name='donor_home'),
    path('login/', views.donor_login, name='login'),
    path('register/', views.donor_register, name='register'),
    path('donor/profile/', views.donor_profile, name='profile'),
    path('available-requests/', views.available_requests, name='available_requests'),
    path('donation-history/', views.donation_history, name='donation_history'),
    path('journey/', views.journey_view, name='journey'),
    path('leaderboard/', views.leaderboard_view, name='leaderboard'),
    path('impact/', views.impact_view, name='impact'),
    path('logout/', views.donor_logout, name='logout'),

    # مسارات تغيير كلمة المرور (مطلوبة ليعمل الزر في صفحة البروفايل)
    path('password-change/', auth_views.PasswordChangeView.as_view(
        template_name='donor/password_change.html',
        success_url='/donor/profile/'
    ), name='password_change'),
    
    path('password-change/done/', auth_views.PasswordChangeDoneView.as_view(
        template_name='donor/password_change_done.html'
    ), name='password_change_done'),
]