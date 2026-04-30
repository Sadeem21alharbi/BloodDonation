from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class DonorProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE) 
    blood_type = models.CharField(max_length=5)
    city = models.CharField(max_length=100)