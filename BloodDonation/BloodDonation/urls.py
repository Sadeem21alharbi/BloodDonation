"""
URL configuration for BloodDonation project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('main.urls')), # تطبيق الصفحة الرئيسية
    path('donor/', include('donor.urls', namespace='donor')), # ربط تطبيق المتبرع
    path('hospital/', include('hospital.urls')), # ربط تطبيق المستشفى
]

# إضافة مسار ملفات الميديا (الصور المرفوعة) ليعمل في بيئة التطوير
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)