from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.http import HttpResponse
from django.contrib import messages
from django.db.models import Sum
from django.db import models  # for models.Q
# or more explicitly:
from django.db.models import Q, Sum
from .models import HospitalProfile, DonationRequest
from .forms import HospitalRegisterForm, HospitalLoginForm, DonationRequestForm
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, Count
from .models import DonorResponse, DonationRequest

# ── 1. Authentication ───────────────────────────────────────────

def hospital_register(request):
    if request.method == 'POST':
        form = HospitalRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('hospital:dashboard')
    else:
        form = HospitalRegisterForm()
    return render(request, 'hospital/hospital_register.html', {'form': form})


def hospital_login(request):
    if request.method == 'POST':
        form = HospitalLoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('hospital:dashboard') # يفضل التوجيه للداشبورد مباشرة
    else:
        form = HospitalLoginForm()
    return render(request, 'hospital/hospital_login.html', {'form': form})


def hospital_logout(request):
    logout(request)
    return redirect('hospital:hospital_login')


# ── 2. Dashboard ─────────────────────────────────────────────────

@login_required
def hospital_dashboard(request):
    hospital = get_object_or_404(HospitalProfile, user=request.user)
    context = {
        'hospital': hospital,
        'total_requests': hospital.total_requests,
        'total_donors': hospital.total_donors,
        'blood_units': hospital.blood_units,
    }
    return render(request, 'hospital/hospital_dashboard.html', context)


# ── 3. Profile (View & Update) ───────────────────────────────────
@login_required
def hospital_profile(request):
    hospital = get_object_or_404(HospitalProfile, user=request.user)

    context = {
        'hospital': hospital,
        'last_updated': hospital.updated_at if hasattr(hospital, 'updated_at') else hospital.user.last_login
    }

    return render(request, 'hospital/hospital_profile.html', context)


@login_required
def hospital_profile_update(request):
    hospital = get_object_or_404(HospitalProfile, user=request.user)

    if request.method == 'POST':

        # ── Basic Info ─────────────────────
        hospital.name = request.POST.get('name_en')
        hospital.name_ar = request.POST.get('name_ar')

        # لو بالمودل اسم الحقل type بدليه هنا
        hospital.type = request.POST.get('hospital_type')

        hospital.health_sector = request.POST.get('health_sector')

        # ── Location ───────────────────────
        hospital.city = request.POST.get('city')
        hospital.district = request.POST.get('district')
        hospital.address = request.POST.get('address')

        # ── Contact ────────────────────────
        hospital.phone = request.POST.get('phone')
        hospital.email = request.POST.get('email')
        hospital.blood_bank_ext = request.POST.get('blood_bank_ext')
        hospital.website = request.POST.get('website')

        # ── Description ────────────────────
        hospital.description = request.POST.get('description')

        # ── Logo Upload ────────────────────
        if request.FILES.get('logo'):
            hospital.logo = request.FILES.get('logo')

        hospital.save()

        messages.success(request, 'Hospital profile updated successfully.')

        return redirect('hospital:profile')

    context = {
        'hospital': hospital
    }

    return render(
        request,
        'hospital/hospital_profile_update.html',
        context
    )

# Donation request management views (create/read/update/delete)

# List of all donation requests
@login_required
def donation_requests(request):
    requests_qs = DonationRequest.objects.all().order_by('-created_at')

    # ── Filters ──────────────────────────────────────────────
    q          = request.GET.get('q', '').strip()
    blood_type = request.GET.get('blood_type', '')
    urgency    = request.GET.get('urgency', '')
    status     = request.GET.get('status', '')

    if q:
        requests_qs = requests_qs.filter(
            models.Q(title__icontains=q) |
            models.Q(department__icontains=q) |
            models.Q(request_type__icontains=q) |
            models.Q(request_id__icontains=q)
        )
    if blood_type:
        requests_qs = requests_qs.filter(blood_type=blood_type)
    if urgency:
        requests_qs = requests_qs.filter(urgency=urgency)
    if status:
        requests_qs = requests_qs.filter(status=status)

    # ── Stats (always on unfiltered full queryset) ────────────
    all_qs = DonationRequest.objects.all()

    context = {
        'requests':        requests_qs,
        'total_requests':  all_qs.count(),
        'active_count':    all_qs.filter(status='active').count(),
        'pending_count':   all_qs.filter(status='pending').count(),
        'inprog_count':    all_qs.filter(status='in_progress').count(),
        'completed_count': all_qs.filter(status='completed').count(),
        'emergency_count': all_qs.filter(urgency='high').count(),
        'total_units':     all_qs.aggregate(t=Sum('required_units'))['t'] or 0,

        # For the blood type dropdown in the filter bar
        'blood_type_choices': DonationRequest.BLOOD_TYPE_CHOICES,
    }

    return render(request, 'hospital/donation_requests.html', context)

# Create new donation request
@login_required
def donation_request_create(request):
    hospital = request.user.hospital_profile

    if request.method == 'POST':
        form = DonationRequestForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.created_by = request.user
            obj.hospital = hospital
            obj.status = 'pending'
            obj.save() # هنا سيتم توليد request_id تلقائياً من الموديل
            
            messages.success(request, 'Donation request created successfully.')
            # التوجيه إلى صفحة التفاصيل (تأكد من مطابقة الاسم في urls.py)
            return redirect('hospital:request_detail', request_id=obj.id)
    else:
        form = DonationRequestForm()

    return render(request, 'hospital/donation_request_create.html', {'form': form})

# View details of a specific donation request
@login_required
def donation_request_detail(request, request_id):
    donation_request = get_object_or_404(DonationRequest, id=request_id)
    return render(request, 'hospital/donation_request_details.html', {'request_obj': donation_request})


# Update an existing donation request
@login_required
def update_donation_request(request, request_id):
    donation_request = get_object_or_404(DonationRequest, id=request_id)

    if request.method == 'POST':
        form = DonationRequestForm(request.POST, instance=donation_request)
        if form.is_valid():
            obj = form.save(commit=False)

            # status is excluded from DonationRequestForm,
            # so we pull it manually from POST and save it ourselves
            new_status = request.POST.get('status')
            valid_statuses = [choice[0] for choice in DonationRequest.STATUS_CHOICES]
            if new_status and new_status in valid_statuses:
                obj.status = new_status

            obj.save()
            messages.success(request, 'Request updated successfully!')
            return redirect('hospital:request_detail', request_id=donation_request.id)
        # if form is invalid, fall through and re-render with errors

    else:
        form = DonationRequestForm(instance=donation_request)

    return render(request, 'hospital/donation_request_update.html', {
        'form': form,
        'request_obj': donation_request,
    })

# Delete a donation request
def delete_donation_request(request, request_id): # غير id إلى request_id
    donation_request = get_object_or_404(DonationRequest, id=request_id)

    if request.method == 'POST':
        donation_request.delete()
        messages.success(request, 'Request deleted successfully.')
        return redirect('hospital:requests')

    return render(request, 'hospital/donation_request_delete.html', {
        'request_obj': donation_request
    })
    
    
# ── List all donor responses ───────────────────────────────────
@login_required
def donor_responses(request):
    responses_qs = DonorResponse.objects.select_related(
        'donor', 'request', 'request__hospital'
    ).all()
 
    # ── Filters ──────────────────────────────────────────────
    q          = request.GET.get('q', '').strip()
    status     = request.GET.get('status', '')
    blood_type = request.GET.get('blood_type', '')
    urgency    = request.GET.get('urgency', '')
 
    if q:
        responses_qs = responses_qs.filter(
            Q(donor__username__icontains=q)      |
            Q(donor__first_name__icontains=q)    |
            Q(donor__last_name__icontains=q)     |
            Q(request__request_id__icontains=q)  |
            Q(request__title__icontains=q)
        )
    if status:
        responses_qs = responses_qs.filter(status=status)
    if blood_type:
        responses_qs = responses_qs.filter(request__blood_type=blood_type)
    if urgency:
        responses_qs = responses_qs.filter(request__urgency=urgency)
 
    # ── Stats (always on full, unfiltered queryset) ───────────
    all_qs = DonorResponse.objects.all()
 
    context = {
        'responses':        responses_qs,
        'total_responses':  all_qs.count(),
        'pending_count':    all_qs.filter(status='pending').count(),
        'inprog_count':     all_qs.filter(status='inprog').count(),
        'accepted_count':   all_qs.filter(status='accepted').count(),
        'rejected_count':   all_qs.filter(status='rejected').count(),
        'completed_count':  all_qs.filter(status='completed').count(),
 
        # For dropdowns
        'blood_type_choices': DonationRequest.BLOOD_TYPE_CHOICES,
        'status_choices':     DonorResponse.STATUS_CHOICES,
    }
 
    return render(request, 'hospital/donor_responses.html', context)
 
 
# ── Detail of a single donor response ─────────────────────────
@login_required
def donor_response_details(request, response_id):
    response_obj = get_object_or_404(
        DonorResponse.objects.select_related('donor', 'request', 'request__hospital'),
        id=response_id
    )
    return render(request, 'hospital/donor_response_details.html', {
        'response_obj': response_obj
    })
 
 
# ── Update response status ─────────────────────────────────────
@login_required
def update_response_status(request, response_id):
    response_obj = get_object_or_404(DonorResponse, id=response_id)
 
    if request.method == 'POST':
        new_status = request.POST.get('status', '').strip()
        valid_statuses = [choice[0] for choice in DonorResponse.STATUS_CHOICES]
 
        if new_status not in valid_statuses:
            messages.error(request, 'Invalid status value.')
            return redirect('hospital:donor_response_detail', response_id=response_obj.id)
 
        old_status = response_obj.status
        response_obj.status = new_status
        response_obj.save()
 
        messages.success(
            request,
            f'Response status updated from "{old_status}" to "{new_status}".'
        )
        # Redirect back to wherever the action came from
        next_url = request.POST.get('next') or request.META.get('HTTP_REFERER')
        if next_url:
            return redirect(next_url)
        return redirect('hospital:donor_responses')
 
    # GET — not expected, redirect away
    return redirect('hospital:donor_responses')
 
 
# ── Delete a donor response ────────────────────────────────────
@login_required
def delete_donor_response(request, response_id):
    response_obj = get_object_or_404(DonorResponse, id=response_id)
 
    if request.method == 'POST':
        response_obj.delete()
        messages.success(request, 'Donor response deleted successfully.')
        return redirect('hospital:donor_responses')
 
    return render(request, 'hospital/donor_response_delete.html', {
        'response_obj': response_obj
    })

# Analytics view
def analytics(request):
    return render(request, 'hospital/analytics.html')

# Settings view
def hospital_settings(request):
    return render(request, 'hospital/hospital_settings.html')