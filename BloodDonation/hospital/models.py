from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class HospitalProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    hospital_name = models.CharField(max_length=200)
    license_number = models.CharField(max_length=50)