from django.shortcuts import render
from django.http import HttpResponse


# Create your views here.
def index(request):
    return render(request, 'index.html')

def log_inn(request):
    return render(request, 'log-inn.html')

def covid_policy(request):
    return render(request,'covid-policy.html')

def locations(request):
    return render(request,'locations.html')

def co2_emissions(request):
    return render(request,'co2-emissions.html')

def prediction(request):
    return render(request,'prediction.html')

def properties(request):
    return render(request,'properties.html')

def create_event(request):
    return render(request,'create-event.html')

def contact(request):
    return render(request,'contact.html')

def four_zero_four(request):
    return render(request,'404.html')

def four_zero_one(request):
    return render(request,'401.html')

def tutorials_and_guides(request):
    return render(request,'tutorials-and-guides.html')

def terms_of_use(request):
    return render(request,'terms-of-use.html')

def privacy_policy(request):
    return render(request,'privacy-policy.html')

def register(request):
    return render(request,'register.html')

def sign_up(request):
    return render(request,'sign-up.html')

def features(request):
    return render(request,'features.html')

def forgotten_password(request):
    return render(request,'forgotten-password.html')

def gamification(request):
    return render(request,'gamification.html')

def reset_password(request):
    return render(request,'reset-password.html')




