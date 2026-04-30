from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate

# Create your views here.

def hospital_login(request):
    return render(request, 'hospital/hospital_login.html')

def hospital_register(request):
    return render(request, 'hospital/hospital_register.html')