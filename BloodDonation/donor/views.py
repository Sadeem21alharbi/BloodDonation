from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from .models import DonorProfile
from .forms import UserUpdateForm, ProfileUpdateForm

# 1. دالة تسجيل مستخدم جديد (مهمة جداً للبدء)
def donor_register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # إنشاء بروفايل فارغ للمستخدم الجديد ليرتبط به لاحقاً
            DonorProfile.objects.create(user=user)
            messages.success(request, 'تم إنشاء الحساب بنجاح! يمكنك تسجيل الدخول الآن.')
            return redirect('donor:donor_login')
    else:
        form = UserCreationForm()
    return render(request, 'donor/donor_register.html', {'form': form})

# 2. دالة تسجيل الدخول (هذه التي سببت الخطأ في image_38.png)
def donor_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('donor:donor_home')
    else:
        form = AuthenticationForm()
    return render(request, 'donor/donor_login.html', {'form': form})

# 3. لوحة التحكم (Dashboard) - الكود الخاص بكِ مع تحسين
@login_required
def donor_dashboard(request):
    profile = request.user.donorprofile
    try:
        donations = profile.donations.all().order_by('-date')[:5] 
    except:
        donations = []
    context = {'profile': profile, 'donations': donations}
    return render(request, 'donor/donor.html', context)

# 4. تعديل البروفايل ورفع الصورة - الكود الخاص بكِ مدمجاً
@login_required
def donor_profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.donorprofile)
        
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, 'تم تحديث بيانات ملفك الشخصي بنجاح!')
            return redirect('donor:profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.donorprofile)

    context = {
        'u_form': u_form,
        'p_form': p_form,
        'profile': request.user.donorprofile
    }
    return render(request, 'donor/profile.html', context)

# 5. تسجيل الخروج
def donor_logout(request):
    logout(request)
    return redirect('main:home')

