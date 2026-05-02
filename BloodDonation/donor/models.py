from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator

class DonorProfile(models.Model):
    # خيارات الجنس والحالة الاجتماعية بناءً على الـ UML
    GENDER_CHOICES = [('M', 'ذكر'), ('F', 'أنثى')]
    MARITAL_CHOICES = [
        ('S', 'أعزب/عزباء'),
        ('M', 'متزوج/ة'),
        ('D', 'مطلق/ة'),
        ('W', 'أرمل/ة')
    ]

    # --- الحقول الإجبارية (المهمة جداً) ---
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # فصيلة الدم والنقاط أساسية لعمل النظام
    blood_type = models.CharField(max_length=5, default="O+", verbose_name="فصيلة الدم")
    points = models.IntegerField(default=0, verbose_name="نقاط العطاء")
    total_donations = models.IntegerField(default=0, verbose_name="إجمالي التبرعات")

    # --- الحقول الاختيارية (تقبل خانات فارغة لتجنب أخطاء الـ Migrate) ---
    id_number = models.CharField(max_length=10, null=True, blank=True, verbose_name="رقم الهوية")
    nationality = models.CharField(max_length=50, null=True, blank=True, verbose_name="الجنسية")
    phone_number = models.CharField(max_length=15, null=True, blank=True, verbose_name="رقم الجوال")
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, null=True, blank=True, verbose_name="الجنس")
    marital_status = models.CharField(max_length=1, choices=MARITAL_CHOICES, null=True, blank=True, verbose_name="الحالة الاجتماعية")
    city = models.CharField(max_length=50, null=True, blank=True, verbose_name="المدينة")
    date_of_birth = models.DateField(null=True, blank=True, verbose_name="تاريخ الميلاد")
    image = models.ImageField(upload_to='donor_profiles/', null=True, blank=True, verbose_name="الصورة الشخصية")
    
    # الوزن اختياري برمجياً لكن عليه فحص (Validator) عند الإدخال
    weight = models.FloatField(null=True, blank=True, validators=[MinValueValidator(50)], verbose_name="الوزن")
    
    lives_saved = models.IntegerField(default=0, verbose_name="أرواح ساهمت بإنقاذها")
    next_donation_date = models.DateField(null=True, blank=True, verbose_name="موعد التبرع القادم")

    # --- منطق المستويات والمزايا (Properties) ---
    @property
    def current_level(self):
        if self.points < 1000: return 'برونز'
        elif self.points < 2000: return 'فضي'
        elif self.points < 3000: return 'ذهبي'
        elif self.points < 4000: return 'بلاتينيوم'
        elif self.points < 5000: return 'ماسي'
        else: return 'النخبة VIP'

    @property
    def get_perks(self):
        level = self.current_level
        perks = {
            'برونز': ['أولوية في مراكز التبرع', 'نقاط ترحيبية مجانية'],
            'فضي': ['مزايا البرونز +', 'خصومات 10% لدى الشركاء الصحيين'],
            'ذهبي': ['مزايا الفضي +', 'فحص شامل دوري مجاني', 'وسام المتبرع الذهبي'],
            'بلاتينيوم': ['مزايا الذهبي +', 'خدمة الموعد السريع', 'دعوات لفعاليات إحياء'],
            'ماسي': ['مزايا البلاتينيوم +', 'لوحة شرف المتميزين', 'هدايا تذكارية فاخرة'],
            'النخبة VIP': ['عضوية النخبة الكاملة', 'خط ساخن مخصص للاستشارات', 'تكريم سنوي']
        }
        return perks.get(level, [])

    @property
    def calculate_progress(self):
        progress = (self.points % 1000) / 10
        return min(progress, 100)

    @property
    def points_needed(self):
        if self.points >= 5000: return 0
        return 1000 - (self.points % 1000)

    def __str__(self):
        return f"{self.user.username} - {self.current_level}"