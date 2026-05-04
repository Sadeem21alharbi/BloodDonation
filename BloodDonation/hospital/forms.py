from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django import forms
from .models import DonationRequest


# Hospital Register Form
class HospitalRegisterForm(UserCreationForm):

    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'البريد الإلكتروني'
        })
    )

    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'اسم المستخدم'
        })
    )

    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'كلمة المرور'
        })
    )

    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'تأكيد كلمة المرور'
        })
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


# Hospital Login Form
class HospitalLoginForm(AuthenticationForm):

    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'اسم المستخدم'
        })
    )

    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'كلمة المرور'
        })
    )
    
# Donation Request Form

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
                'placeholder': 'e.g. Emergency O− Blood Required — ICU'
            }),

            'request_type': forms.Select(attrs={
                'class': 'rq-select-f'
            }),

            'blood_type': forms.Select(attrs={
                'class': 'rq-select-f'
            }),

            'required_units': forms.NumberInput(attrs={
                'class': 'rq-input',
                'placeholder': 'e.g. 4',
                'min': 1,
                'max': 50
            }),

            'urgency': forms.Select(attrs={
                'class': 'rq-select-f'
            }),

            'department': forms.Select(attrs={
                'class': 'rq-select-f'
            }),

            'patient_condition': forms.Select(attrs={
                'class': 'rq-select-f'
            }),

            'required_before': forms.DateInput(attrs={
                'class': 'rq-input',
                'type': 'date'
            }),

            'expired_date': forms.DateTimeInput(attrs={
                'class': 'rq-input',
                'type': 'datetime-local'
            }),

            'contact_number': forms.TextInput(attrs={
                'class': 'rq-input',
                'placeholder': '+966 5X XXX XXXX'
            }),

            'assigned_staff': forms.TextInput(attrs={
                'class': 'rq-input',
                'placeholder': 'Dr. Ahmed'
            }),

            'patient_file_number': forms.TextInput(attrs={
                'class': 'rq-input',
                'placeholder': 'Patient File Number'
            }),

            'notes': forms.Textarea(attrs={
                'class': 'rq-textarea',
                'placeholder': 'Additional medical notes...',
                'rows': 4
            }),
        }