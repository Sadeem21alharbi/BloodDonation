from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum


class HospitalProfile(models.Model):

    HOSPITAL_TYPES = [
        ('university', 'University Hospital'),
        ('general',    'General Hospital'),
        ('specialist', 'Specialist Hospital'),
        ('private',    'Private Hospital'),
        ('military',   'Military Hospital'),
        ('national',   'National Guard'),
        ('maternity',  'Maternity & Children'),
        ('clinic',     'Medical Clinic'),
    ]

    HEALTH_SECTORS = [
        ('MOH',        'Ministry of Health'),
        ('NGHA',       'National Guard (NGHA)'),
        ('MOD',        'Ministry of Defense'),
        ('KFSH',       'King Faisal Specialist'),
        ('private',    'Private Sector'),
        ('university', 'University Sector'),
        ('other',      'Other'),
    ]

    user           = models.OneToOneField(User, on_delete=models.CASCADE, related_name='hospital_profile')
    name           = models.CharField(max_length=200)
    name_ar        = models.CharField(max_length=200, blank=True)
    hospital_type  = models.CharField(max_length=30, choices=HOSPITAL_TYPES, default='general')
    health_sector  = models.CharField(max_length=30, choices=HEALTH_SECTORS, default='MOH')
    city           = models.CharField(max_length=100, default='Riyadh')
    district       = models.CharField(max_length=100, blank=True)
    address        = models.TextField(blank=True)
    phone          = models.CharField(max_length=20, blank=True)
    email          = models.EmailField(blank=True)
    website        = models.URLField(blank=True)
    blood_bank_ext = models.CharField(max_length=20, blank=True)
    description    = models.TextField(blank=True, max_length=500)
    logo           = models.ImageField(upload_to='hospital_logos/', blank=True, null=True)
    is_verified    = models.BooleanField(default=False)
    joined_date    = models.DateField(auto_now_add=True)

    notif_emergency = models.BooleanField(default=True)
    notif_responses = models.BooleanField(default=True)
    notif_weekly    = models.BooleanField(default=False)
    notif_sms       = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    @property
    def initials(self):
        words = self.name.split()
        return ''.join(w[0].upper() for w in words[:2])

    @property
    def total_requests(self):
        return self.blood_requests.count()

    @property
    def total_donors(self):
        return DonorResponse.objects.filter(
            request__hospital=self
        ).values('donor').distinct().count()

    @property
    def blood_units(self):
        total = self.blood_requests.filter(
            status='completed'
        ).aggregate(Sum('required_units'))['required_units__sum'] or 0
        return f'{total / 1000:.1f}K' if total >= 1000 else str(total)


class DonationRequest(models.Model):


   REQUEST_TYPE_CHOICES = [
       ('emergency',  'Emergency Case'),
       ('blood_bank', 'Blood Bank Refill'),
       ('surgical',   'Surgical Preparation'),
       ('plasma',     'Plasma Donation'),
       ('platelets',  'Platelet Donation'),
       ('other',      'Other'),
   ]


   BLOOD_TYPE_CHOICES = [
       ('A+', 'A+'), ('A-', 'A-'),
       ('B+', 'B+'), ('B-', 'B-'),
       ('AB+', 'AB+'), ('AB-', 'AB-'),
       ('O+', 'O+'), ('O-', 'O-'),
   ]


   URGENCY_CHOICES = [
       ('high',   'High'),
       ('medium', 'Medium'),
       ('low',    'Low'),
   ]


   STATUS_CHOICES = [
       ('pending',     'Pending'),
       ('in_progress', 'In Progress'),
       ('active',      'Active'),
       ('completed',   'Completed'),
       ('closed',      'Closed'),
       ('cancelled',   'Cancelled'),
       ('emergency',   'Emergency'),
   ]


   DEPARTMENT_CHOICES = [
       ('ICU',        'ICU'),
       ('ER',         'Emergency Room'),
       ('OR',         'Operating Room'),
       ('Pediatrics', 'Pediatrics'),
       ('Oncology',   'Oncology'),
       ('Maternity',  'Maternity'),
       ('General',    'General Ward'),
       ('Blood Bank', 'Blood Bank'),
   ]


   PATIENT_CONDITION_CHOICES = [
       ('critical',  'Critical'),
       ('serious',   'Serious'),
       ('stable',    'Stable'),
       ('elective',  'Elective / Scheduled'),
   ]


   # FK to hospital — required so HospitalProfile.blood_requests works
   hospital = models.ForeignKey(
       HospitalProfile,
       on_delete=models.CASCADE,
       related_name='blood_requests',
   )


   created_by = models.ForeignKey(
       User,
       on_delete=models.CASCADE,
       related_name='donation_requests',
   )


   request_id = models.CharField(max_length=20, unique=True, blank=True)
   title      = models.CharField(max_length=255)


   request_type      = models.CharField(max_length=20, choices=REQUEST_TYPE_CHOICES)
   blood_type        = models.CharField(max_length=5,  choices=BLOOD_TYPE_CHOICES)
   required_units    = models.PositiveIntegerField()
   urgency           = models.CharField(max_length=10, choices=URGENCY_CHOICES)
   status            = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
   department        = models.CharField(max_length=50, choices=DEPARTMENT_CHOICES)
   patient_condition = models.CharField(max_length=20, choices=PATIENT_CONDITION_CHOICES, blank=True, null=True)
   required_before   = models.DateField(blank=True, null=True)
   contact_number    = models.CharField(max_length=20, blank=True)
   notes             = models.TextField(blank=True)
   assigned_staff    = models.CharField(max_length=150, blank=True)
   patient_file_number = models.CharField(max_length=100, blank=True, null=True)


   # Progress tracking
   fulfilled_units    = models.PositiveIntegerField(default=0)
   total_responses    = models.PositiveIntegerField(default=0)
   accepted_responses = models.PositiveIntegerField(default=0)
   rejected_responses = models.PositiveIntegerField(default=0)
   pending_responses  = models.PositiveIntegerField(default=0)


   created_at = models.DateTimeField(auto_now_add=True)
   updated_at = models.DateTimeField(auto_now=True)


   class Meta:
       ordering = ['-created_at']


   def __str__(self):
       return f'{self.request_id} - {self.title}'


   @property
   def donor_responses_count(self):
       return self.responses.count()


   @property
   def completion_percentage(self):
       if self.required_units == 0:
           return 0
       return int((self.fulfilled_units / self.required_units) * 100)


   def save(self, *args, **kwargs):
       if not self.request_id:
           last = DonationRequest.objects.order_by('-id').first()
           next_id = (last.id + 1) if last else 1
           self.request_id = f'REQ-{next_id:04d}'
       super().save(*args, **kwargs)
       
       
class DonorResponse(models.Model):

    STATUS_CHOICES = [
        ('pending',   'Pending'),
        ('inprog',    'In Progress'),
        ('accepted',  'Accepted'),
        ('rejected',  'Rejected'),
        ('completed', 'Completed'),
    ]

    request      = models.ForeignKey(DonationRequest, on_delete=models.CASCADE, related_name='responses')
    donor        = models.ForeignKey(User, on_delete=models.CASCADE, related_name='hospital_responses')
    status       = models.CharField(max_length=15, choices=STATUS_CHOICES, default='pending')
    notes        = models.TextField(blank=True)
    responded_at = models.DateTimeField(auto_now_add=True)
    updated_at   = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-responded_at']

    def __str__(self):
        return f'Response by {self.donor.username} for {self.request}'