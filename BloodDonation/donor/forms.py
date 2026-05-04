from django import forms
from .models import DonorProfile
from django.contrib.auth.models import User

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }

from django import forms
from .models import DonorProfile
from django.contrib.auth.models import User

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }

class ProfileUpdateForm(forms.ModelForm):
    # خيارات نعم/لا للأمراض والأدوية
    CHRONIC_CHOICES = [('no', 'لا'), ('yes', 'نعم')]
    
    # خيارات فصيلة الدم التي طلبتِها
    BLOOD_TYPES = [
        ('', 'اختر فصيلة الدم'), # خيار فارغ في البداية
        ('A+', 'A+'), ('A-', 'A-'),
        ('B+', 'B+'), ('B-', 'B-'),
        ('AB+', 'AB+'), ('AB-', 'AB-'),
        ('O+', 'O+'), ('O-', 'O-'),
    ]

    # تعريف الحقول الإضافية
    has_chronic = forms.ChoiceField(choices=CHRONIC_CHOICES, label="هل تعاني من أمراض مزمنة؟")
    takes_meds = forms.ChoiceField(choices=CHRONIC_CHOICES, label="هل تتناول أي أدوية؟")
    
    # تحويل فصيلة الدم لقائمة اختيار
    blood_type = forms.ChoiceField(choices=BLOOD_TYPES, label="فصيلة الدم")

    class Meta:
        model = DonorProfile
        fields = [
            'id_number', 'nationality', 'phone_number', 
            'gender', 'marital_status', 'city', 
            'date_of_birth', 'blood_type', 'weight', 
            'chronic_disease_type', 'medication_type', 'image'
        ]
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'id_number': forms.TextInput(attrs={'class': 'form-control'}),
            'nationality': forms.TextInput(attrs={'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            'gender': forms.Select(attrs={'class': 'form-control'}),
            'marital_status': forms.Select(attrs={'class': 'form-control'}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
            'blood_type': forms.Select(attrs={'class': 'form-control'}), # سيظهر كقائمة منسدلة
            'weight': forms.NumberInput(attrs={'class': 'form-control'}),
            'chronic_disease_type': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'اذكر نوع المرض'}),
            'medication_type': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'اذكر نوع الدواء'}),
        }

    def __init__(self, *args, **kwargs):
        super(ProfileUpdateForm, self).__init__(*args, **kwargs)
        # جعل حقول التفاصيل غير إجبارية لكي لا يتعطل الفورم عند إخفائها في الواجهة
        self.fields['chronic_disease_type'].required = False
        self.fields['medication_type'].required = False
        
        # إضافة كلاس form-control لحقول الـ ChoiceField يدوياً لضمان التناسق
        self.fields['has_chronic'].widget.attrs.update({'class': 'form-control'})
        self.fields['takes_meds'].widget.attrs.update({'class': 'form-control'})