from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import HospitalProfile
from .models import DonationRequest 

# ── Register ──────────────────────────────────────────────────
class HospitalRegisterForm(UserCreationForm):

    hospital_name = forms.CharField(
        max_length=200,
        label='Hospital Name',
        widget=forms.TextInput(attrs={
            'class': 'rq-input',
            'placeholder': 'King Khalid University Hospital',
        })
    )

    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'rq-input',
            'placeholder': 'contact@hospital.com',
        })
    )

    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'rq-input',
            'placeholder': 'اسم المستخدم',
        })
    )

    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'rq-input',
            'placeholder': 'كلمة المرور',
        })
    )

    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'rq-input',
            'placeholder': 'تأكيد كلمة المرور',
        })
    )

    class Meta:
        model  = User
        fields = ['username', 'hospital_name', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            HospitalProfile.objects.create(
                user=user,
                name=self.cleaned_data['hospital_name'],
                email=self.cleaned_data['email'],
            )
        return user


# ── Login ──────────────────────────────────────────────────────
class HospitalLoginForm(AuthenticationForm):

    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'rq-input',
            'placeholder': 'اسم المستخدم',
        })
    )

    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'rq-input',
            'placeholder': 'كلمة المرور',
        })
    )
    
    
    # ── Donation Request ───────────────────────────────────────────
class DonationRequestForm(forms.ModelForm):


   class Meta:
       model = DonationRequest
       exclude = [
           'hospital',
           'request_id',
           'created_at',
           'updated_at',
           'status',
           'created_by',
           'fulfilled_units',
           'total_responses',
           'accepted_responses',
           'rejected_responses',
           'pending_responses',
       ]
       widgets = {
           'title': forms.TextInput(attrs={
               'class': 'rq-input',
               'placeholder': 'e.g. Emergency O− Blood Required — ICU',
           }),
           'request_type': forms.Select(attrs={'class': 'rq-select-f'}),
           'blood_type':   forms.Select(attrs={'class': 'rq-select-f'}),
           'required_units': forms.NumberInput(attrs={
               'class': 'rq-input',
               'placeholder': 'e.g. 4',
               'min': 1,
               'max': 50,
           }),
           'urgency':           forms.Select(attrs={'class': 'rq-select-f'}),
           'department':        forms.Select(attrs={'class': 'rq-select-f'}),
           'patient_condition': forms.Select(attrs={'class': 'rq-select-f'}),
           'required_before': forms.DateInput(attrs={
               'class': 'rq-input',
               'type': 'date',
           }),
           'contact_number': forms.TextInput(attrs={
               'class': 'rq-input',
               'placeholder': '+966 5X XXX XXXX',
           }),
           'assigned_staff': forms.TextInput(attrs={
               'class': 'rq-input',
               'placeholder': 'Dr. Ahmed',
           }),
           'patient_file_number': forms.TextInput(attrs={
               'class': 'rq-input',
               'placeholder': 'Patient File Number',
           }),
           'notes': forms.Textarea(attrs={
               'class': 'rq-textarea',
               'placeholder': 'Additional medical notes...',
               'rows': 4,
           }),
       }


# ── Hospital Profile ───────────────────────────────────────────
class HospitalProfileForm(forms.ModelForm):
    class Meta:
        model = HospitalProfile
        fields = ['name', 'name_ar', 'hospital_type', 'health_sector', 'city', 'district', 'address', 'phone', 'email', 'website', 'blood_bank_ext', 'description', 'logo']

