from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from .forms import HospitalRegisterForm, HospitalLoginForm, DonationRequestForm 
from .models import DonationRequest

# Create your views here.

# Hospital Authentication Views (Login/Register/Logout)

# Register view
def hospital_register(request):

    if request.method == 'POST':
        form = HospitalRegisterForm(request.POST)

        if form.is_valid():
            user = form.save()

            login(request, user)

            return redirect('hospital:hospital_dashboard')

    else:
        form = HospitalRegisterForm()

    context = {
        'form': form
    }

    return render(
        request,
        'hospital/hospital_register.html',
        context
    )

# Login view    
def hospital_login(request):

    if request.method == 'POST':

        form = HospitalLoginForm(
            request,
            data=request.POST
        )

        if form.is_valid():

            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            user = authenticate(
                request,
                username=username,
                password=password
            )

            if user is not None:
                login(request, user)

                return redirect(
                    'hospital:hospital_dashboard'
                )

    else:
        form = HospitalLoginForm()

    context = {
        'form': form
    }

    return render(
        request,
        'hospital/hospital_login.html',
        context
    )

# Logout view
def hospital_logout(request):

    logout(request)

    return redirect('hospital:login')

# Hospital Dashboard Views

# Main dashboard view
def hospital_dashboard(request):
    return render(request, 'hospital/hospital_dashboard.html')

# Profile views (view/update/delete
def hospital_profile(request):
    return render(request, 'hospital/hospital_profile.html')

def hospital_profile_update(request):
    return render(request, 'hospital/hospital_profile_update.html')

# Donation request management views (create/read/update/delete)
def donation_requests(request):

    requests_qs = DonationRequest.objects.all().order_by('-created_at')

    form = DonationRequestForm()

    context = {
        'requests': requests_qs,
        'form': form,
        'total_requests': requests_qs.count(),
    }

    return render(request, 'hospital/donation_requests.html', context)

def request_create(request):
    hospital = request.user.hospital_profile

    if request.method == 'POST':
        form = DonationRequestForm(request.POST)

        if form.is_valid():
            obj = form.save(commit=False)

            obj.created_by = request.user   # 🔥 مهم جدًا
            obj.status = 'pending'          # default manual
            obj.total_responses = 0
            obj.accepted_responses = 0
            obj.rejected_responses = 0
            obj.pending_responses = 0

            obj.save()

            return redirect('hospital:requests')

        else:
            print("FORM ERRORS:", form.errors)  # مهم للتشخيص

    else:
        form = DonationRequestForm()

    requests_qs = DonationRequest.objects.all()

    return render(request, 'hospital/donation_requests.html', {
        'form': form,
        'requests': requests_qs,
        'total_requests': requests_qs.count(),
    })

def donation_request_detail(request, id):
    return render(request, 'hospital/donation_request_detail.html')

def update_donation_request(request, id):
    return render(request, 'hospital/update_donation_request.html')

def delete_donation_request(request, id):
    return render(request, 'hospital/delete_donation_request.html')

# Donor response management view
def donor_responses(request):
    return render(request, 'hospital/donor_responses.html')

def update_response_status(request, id):
    return render(request, 'hospital/update_response_status.html')

# Analytics view
def analytics(request):
    return render(request, 'hospital/analytics.html')

# Settings view
def hospital_settings(request):
    return render(request, 'hospital/hospital_settings.html')