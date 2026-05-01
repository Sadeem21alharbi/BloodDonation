from django.db import models
from django.contrib.auth.models import User


# Create your models here.


class DonorProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE) # ربط الملف بالمستخدم
    blood_type = models.CharField(max_length=5)
    total_donations = models.IntegerField(default=0)
    lives_saved = models.IntegerField(default=0)
    next_donation_date = models.DateField(null=True, blank=True)
    points = models.IntegerField(default=0)

    @property
    def calculate_progress(self):
        max_points = 1000
        if self.points >= max_points:
            return 100
        return (self.points / max_points) * 100

    @property
    def points_needed(self):
        return 1000 - self.points

    def __str__(self):
        return self.user.username
    

