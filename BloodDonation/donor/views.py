from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from .models import DonorProfile, DonationRecord  
from hospital.models import DonationRequest, DonorResponse

def donor_register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # إنشاء بروفايل فارغ للمستخدم الجديد لربطه بالبيانات اللاحقة
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
    # جلب بروفايل المستخدم المسجل أو إنشاؤه إذا لم يوجد
    profile, created = DonorProfile.objects.get_or_create(user=request.user)
    
    # جلب آخر 5 تبرعات للمستخدم الحالي لعرضها في لوحة التحكم
    donations = DonationRecord.objects.filter(donor=request.user).order_by('-date')[:5]
    
    context = {
        'profile': profile, 
        'donations': donations
    }
    return render(request, 'donor/donor.html', context)

@login_required
def donor_profile(request):
    # استيراد الفورمز داخل الدالة لتجنب التكرار أو أخطاء الاستيراد الدائري
    from .forms import UserUpdateForm, ProfileUpdateForm 
    
    if request.method == 'POST':
        # معالجة طلب حذف الحساب نهائياً
        if 'delete_account' in request.POST:
            user = request.user
            logout(request) # تسجيل الخروج أولاً
            user.delete()   # حذف المستخدم من قاعدة البيانات
            messages.warning(request, 'تم حذف حسابك الشخصي وكافة بياناتك بنجاح.')
            return redirect('main:home') # التوجه للصفحة الرئيسية للموقع

        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.donorprofile)
        
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, 'تم حفظ تعديلات ملفك الشخصي بنجاح.')
            return redirect('donor:profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.donorprofile)

    context = {
        'u_form': u_form,
        'p_form': p_form,
        'profile': request.user.donorprofile # ضروري لعرض تاريخ آخر تحديث وصورة البروفايل
    }
    return render(request, 'donor/profile.html', context)

def donor_logout(request):
    logout(request)
    messages.info(request, 'تم تسجيل الخروج بنجاح. ننتظر عودتك قريباً!')
    return redirect('main:home')

def available_requests(request):
    # جلب كل الطلبات بغض النظر عن الحالة ليظهر طلبك الجديد
    queryset = DonationRequest.objects.all().order_by('-created_at')

    # نظام التصفية (الفلترة)
    city_query = request.GET.get('city')
    blood_query = request.GET.get('blood_type')
    urgency_query = request.GET.get('urgency')

    if city_query:
        queryset = queryset.filter(hospital__city__icontains=city_query)
    if blood_query:
        queryset = queryset.filter(blood_type=blood_query)
    if urgency_query:
        queryset = queryset.filter(urgency=urgency_query)

    context = {
        'blood_requests': queryset,
        'urgent_requests_count': queryset.filter(urgency='urgent').count(),
        'cities': ['الرياض', 'جدة', 'الدمام', 'مكة المكرمة', 'المدينة المنورة', 'أبها', 'تبوك'],
        'blood_types': ['O+', 'O-', 'A+', 'A-', 'B+', 'B-', 'AB+', 'AB-']
    }
    return render(request, 'donor/available_requests.html', context)

@login_required
def donation_history(request):
    # عرض كافة سجلات التبرع السابقة للمتبرع
    donations = DonationRecord.objects.filter(donor=request.user).order_by('-date')
    return render(request, 'donor/donation_history.html', {'donations': donations})

def journey_view(request):
    return render(request, 'donor/journey.html')

def leaderboard_view(request):
    # عرض المتصدرين بناءً على النقاط (تحفيز المتبرعين)
    top_donors = DonorProfile.objects.all().order_by('-points')[:10]
    return render(request, 'donor/leaderboard.html', {'top_donors': top_donors})

def impact_view(request):
    return render(request, 'donor/impact.html')

@login_required
def apply_to_request(request, request_id):
    # جلب الطلب المحدد
    donation_request = DonationRequest.objects.get(id=request_id)
    
    # التأكد أن المتبرع لم يقدم على هذا الطلب من قبل
    already_applied = DonorResponse.objects.filter(request=donation_request, donor=request.user).exists()
    
    if not already_applied:
        # إنشاء التقديم (الربط بينك وبين الطلب)
        DonorResponse.objects.create(
            request=donation_request,
            donor=request.user,
            status='pending'
        )
        messages.success(request, 'تم إرسال طلب التقديم للمستشفى بنجاح!')
    else:
        messages.warning(request, 'لقد قمت بالتقديم على هذا الطلب مسبقاً.')
        
    return redirect('donor:available_requests')