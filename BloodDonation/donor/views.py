from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate

# Create your views here.


def donor_login(request):
    return render(request, 'donor/donor_login.html')

def donor_register(request):
    return render(request, 'donor/donor_register.html')