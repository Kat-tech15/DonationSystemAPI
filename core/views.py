from django.shortcuts import render,redirect
from .models import ContactMessage
from django.contrib import messages

def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')
    
def services(request):
    return render(request, 'services.html')

def contact(request):
    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        email = request.POST.get('email')
        message = request.POST.get('message')

        contact =  ContactMessage.objects.create(
            full_name =full_name,
            email= email,
            message= message,
        )
        contact.save()
        messages.success = (request, 'Your message was submitted successfully.')
    return render(request, 'contact.html')