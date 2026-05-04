from django.db import models
from django.contrib.auth.models import User
import uuid

# Create your models here.

class HospitalProfile(models.Model):

    # ========== RELATION ==========
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # ========== BASIC INFO ==========
    name_ar = models.CharField(max_length=255)  # اسم المستشفى بالعربي
    name_en = models.CharField(max_length=255, blank=True, null=True)

    license_number = models.CharField(max_length=50)

    # ========== CLASSIFICATION ==========
    HEALTH_SECTOR_CHOICES = [
        ('MOH', 'Ministry of Health (MOH)'),
        ('NGHA', 'National Guard (NGHA)'),
        ('MOD', 'Ministry of Defense (MOD)'),
        ('KFSH', 'King Faisal Specialist (KFSH)'),
        ('PRIVATE', 'Private Sector'),
        ('UNIVERSITY', 'University Sector'),
        ('OTHER', 'Other'),
    ]

    hospital_type = models.CharField(
        max_length=50,
        choices=HEALTH_SECTOR_CHOICES,
        default='MOH'
    )

    health_sector = models.CharField(
        max_length=50,
        choices=HEALTH_SECTOR_CHOICES,
        default='MOH'
    )

    # ========== CONTACT INFO ==========
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    website = models.URLField(blank=True, null=True)

    # ========== LOCATION ==========
    city = models.CharField(max_length=100)
    district = models.CharField(max_length=100, blank=True, null=True)
    full_address = models.TextField(blank=True, null=True)

    # ========== ABOUT ==========
    description = models.TextField(blank=True, null=True)

    # ========== META ==========
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name_ar


class DonationRequest(models.Model):
    
    # Choices

    REQUEST_TYPE_CHOICES = [
        ('emergency', 'Emergency Case'),
        ('blood_bank', 'Blood Bank Refill'),
        ('surgical', 'Surgical Preparation'),
        ('plasma', 'Plasma Donation'),
        ('platelets', 'Platelet Donation'),
        ('other', 'Other'),
    ]

    BLOOD_TYPE_CHOICES = [
        ('A+', 'A+'),
        ('A-', 'A-'),
        ('B+', 'B+'),
        ('B-', 'B-'),
        ('AB+', 'AB+'),
        ('AB-', 'AB-'),
        ('O+', 'O+'),
        ('O-', 'O-'),
    ]

    URGENCY_CHOICES = [
        ('high', 'High'),
        ('medium', 'Medium'),
        ('low', 'Low'),
    ]

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('closed', 'Closed'),
    ]

    DEPARTMENT_CHOICES = [
        ('ICU', 'ICU'),
        ('ER', 'Emergency Room'),
        ('OR', 'Operating Room'),
        ('Pediatrics', 'Pediatrics'),
        ('Oncology', 'Oncology'),
        ('Maternity', 'Maternity'),
        ('General', 'General Ward'),
        ('Blood Bank', 'Blood Bank'),
    ]

    PATIENT_CONDITION_CHOICES = [
        ('critical', 'Critical'),
        ('serious', 'Serious'),
        ('stable', 'Stable'),
        ('elective', 'Elective / Scheduled'),
    ]


    # Main Information
    
    request_id = models.CharField(
        max_length=20,
        unique=True,
        blank=True
    )

    title = models.CharField(
        max_length=255
    )

    request_type = models.CharField(
        max_length=20,
        choices=REQUEST_TYPE_CHOICES
    )

    blood_type = models.CharField(
        max_length=5,
        choices=BLOOD_TYPE_CHOICES
    )

    required_units = models.PositiveIntegerField()

    urgency = models.CharField(
        max_length=10,
        choices=URGENCY_CHOICES
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )
    
    created_at = models.DateTimeField(
        auto_now_add=True
    )

    # Hospital & Patient Details

    department = models.CharField(
        max_length=50,
        choices=DEPARTMENT_CHOICES
    )

    patient_condition = models.CharField(
        max_length=20,
        choices=PATIENT_CONDITION_CHOICES,
        blank=True,
        null=True
    )

    required_before = models.DateField(
        blank=True,
        null=True
    )

    contact_number = models.CharField(
        max_length=20,
        blank=True
    )

    notes = models.TextField(
        blank=True
    )

    # Added Fields

    assigned_staff = models.CharField(
        max_length=150,
        help_text='Doctor or staff responsible for this case'
    )

    patient_file_number = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text='Optional for blood bank refill requests'
    )

    # Tracking

    created_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='donation_requests'
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    # Progress Tracking


    fulfilled_units = models.PositiveIntegerField(
        default=0
    )

    total_responses = models.PositiveIntegerField(
        default=0
    )

    accepted_responses = models.PositiveIntegerField(
        default=0
    )

    rejected_responses = models.PositiveIntegerField(
        default=0
    )

    pending_responses = models.PositiveIntegerField(
        default=0
    )

    # Model Methods

    def __str__(self):
        return f"{self.request_id} - {self.title}"


    @property
    def completion_percentage(self):

        if self.required_units == 0:
            return 0

        return int(
            (self.fulfilled_units / self.required_units) * 100
        )


    def save(self, *args, **kwargs):

        if not self.request_id:

            last_request = DonationRequest.objects.order_by('-id').first()

            if last_request:
                last_id = last_request.id + 1
            else:
                last_id = 1

            self.request_id = f"REQ-{last_id:04d}"

        super().save(*args, **kwargs)