from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from .models import DonorProfile, DonationRecord  

def donor_register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # إنشاء بروفايل فارغ للمستخدم الجديد
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
    # جلب البروفايل الخاص بالمستخدم المسجل
    profile, created = DonorProfile.objects.get_or_create(user=request.user)
    
    # التعديل هنا: نستخدم request.user مباشرة لأنه هو الـ "User instance" المطلوب
    donations = DonationRecord.objects.filter(donor=request.user).order_by('-date')[:5]
    
    context = {
        'profile': profile, 
        'donations': donations
    }
    return render(request, 'donor/donor.html', context)

@login_required
def donor_profile(request):
    from .forms import UserUpdateForm, ProfileUpdateForm 
    
    if request.method == 'POST':
        if 'delete_account' in request.POST:
            user = request.user
            logout(request)
            user.delete()
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

def available_requests(request):
    try:
        from .models import BloodRequest 
        queryset = BloodRequest.objects.all().order_by('-is_urgent', '-id')
    except ImportError:
        queryset = []

    city_query = request.GET.get('city')
    blood_query = request.GET.get('blood_type')
    urgency_query = request.GET.get('urgency')

    if city_query:
        queryset = queryset.filter(city__icontains=city_query)
    if blood_query:
        queryset = queryset.filter(blood_type=blood_query)
    if urgency_query == 'urgent':
        queryset = queryset.filter(is_urgent=True)

    urgent_count = 0
    if queryset:
        urgent_count = queryset.filter(is_urgent=True).count()

    context = {'blood_requests': queryset,
        'urgent_requests_count': urgent_count,
        'cities': BloodRequest.objects.values_list('city', flat=True).distinct() if queryset else [],
        'blood_types': ['O+', 'O-', 'A+', 'A-', 'B+', 'B-', 'AB+', 'AB-']
    }
    return render(request, 'donor/available_requests.html', context)

@login_required
def donation_history(request):
    # التعديل هنا أيضاً: نستخدم request.user لضمان المطابقة مع نوع الحقل في قاعدة البيانات
    donations = DonationRecord.objects.filter(donor=request.user).order_by('-date')
    return render(request, 'donor/donation_history.html', {'donations': donations})

def journey_view(request):
    return render(request, 'donor/journey.html')

def leaderboard_view(request):
    top_donors = DonorProfile.objects.all().order_by('-points')[:10]
    return render(request, 'donor/leaderboard.html', {'top_donors': top_donors})

def impact_view(request):
    return render(request, 'donor/impact.html')