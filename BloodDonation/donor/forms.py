from django import forms
from .models import DonorProfile
from django.contrib.auth.models import User

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = DonorProfile
        fields = [
            'id_number', 'nationality', 'phone_number', 
            'gender', 'marital_status', 'city', 
            'date_of_birth', 'blood_type', 'weight', 'image'
        ]
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
        }