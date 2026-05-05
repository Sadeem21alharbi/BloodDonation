from django.urls import path
from . import views

app_name='main'

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name="about"),
    path('how its work/', views.works, name="works"),
    path('questions/', views.faq, name="faq"),
    path('donor guide/', views.guide, name="guide"),
    path('privacy/', views.privacy, name="privacy"),
    path('terms/', views.terms, name="terms")
]