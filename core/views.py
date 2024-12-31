from django.shortcuts import render

# Create your views here.

def home(request):
    return render(request, 'core/home.html')

def services(request):
    return render(request, 'core/services.html')

def appointments(request):
    return render(request, 'core/appointments.html')

def queue(request):
    return render(request, 'core/queue.html')