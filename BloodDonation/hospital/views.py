from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate

# Create your views here.

def hospital_login(request):
    return render(request, 'hospital/hospital_login.html')


def hospital_register(request):
    return render(request, 'hospital/hospital_register.html')


def hospital_dashboard(request):
    return render(request, 'hospital/hospital_dashboard.html')


def hospital_profile(request):
    return render(request, 'hospital/hospital_profile.html')

def donation_requests(request):
    return render(request, 'hospital/donation_requests.html')


def donor_responses(request):
    return render(request, 'hospital/donor_responses.html')


def analytics(request):
    return render(request, 'hospital/analytics.html')


def settings(request):
    return render(request, 'hospital/settings.html')