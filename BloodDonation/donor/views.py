from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from .models import DonorProfile

@login_required(login_url='donor:login')
def donor_dashboard(request):
    # استخدام get_or_create يجعل الكود أقصر وأكثر احترافية
    profile, created = DonorProfile.objects.get_or_create(user=request.user)
    return render(request, 'donor/donor.html', {'profile': profile})

def donor_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('donor:dashboard')
    else:
        form = AuthenticationForm()
    return render(request, "donor/donor_login.html", {'form': form})

def donor_register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # التأكد من إنشاء البروفايل للمستخدم الجديد
            DonorProfile.objects.get_or_create(user=user)
            login(request, user)
            return redirect('donor:dashboard')
    else:
        form = UserCreationForm()
    return render(request, "donor/donor_register.html", {'form': form})