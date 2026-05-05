from django.shortcuts import render

# Create your views here.

def home(request):
    return render(request, 'main/home.html')

def about(request):
        return render(request, 'main/about.html')

def works(request):
        return render(request, 'main/works.html')

def faq(request):
        return render(request, 'main/faq.html')

def guide(request):
        return render(request, 'main/donor_guide.html')

def terms(request):
        return render(request, 'main/terms_and_conditions.html')

def privacy(request):
        return render(request, 'main/privacy_policy.html')


