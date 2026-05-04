
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from .models import DonorProfile
from .forms import UserUpdateForm, ProfileUpdateForm

def donor_register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # إنشاء بروفايل فارغ للمستخدم الجديد ليرتبط به لاحقاً
            DonorProfile.objects.create(user=user)
            messages.success(request, 'تم إنشاء الحساب بنجاح! يمكنك تسجيل الدخول الآن.')
            return redirect('donor:login')
    else:
        form = UserCreationForm()
    return render(request, 'donor/donor_register.html', {'form': form})

def donor_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f'مرحباً بك مجدداً يا {username}!')
                return redirect('donor:donor_home')
            else:
                messages.error(request, 'خطأ في اسم المستخدم أو كلمة المرور.')
        else:
            messages.error(request, 'بيانات تسجيل الدخول غير صحيحة.')
    else:
        form = AuthenticationForm()
    return render(request, 'donor/donor_login.html', {'form': form})

@login_required
def donor_dashboard(request):
    profile = request.user.donorprofile
    try:
        donations = profile.donations.all().order_by('-date')[:5] 
    except:
        donations = []
    context = {'profile': profile, 'donations': donations}
    return render(request, 'donor/donor.html', context)

@login_required
def donor_profile(request):
    if request.method == 'POST':
        # التحقق إذا كان المستخدم ضغط على زر الحذف (إذا قمتِ بتسمية الزر delete_account)
        if 'delete_account' in request.POST:
            user = request.user
            logout(request) # تسجيل الخروج أولاً
            user.delete()   # حذف المستخدم من قاعدة البيانات
            messages.warning(request, 'تم حذف حسابك الشخصي بنجاح.')
            return redirect('main:home')

        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.donorprofile)
        
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, 'تم حفظ البيانات بنجاح')
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

def donor_logout(request):
    logout(request)
    messages.info(request, 'تم تسجيل الخروج بنجاح.')
    return redirect('main:home')
