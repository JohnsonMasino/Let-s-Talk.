
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from NinazHairline.forms import SubscribeForm
from .models import Service, Topic
from .forms import ServiceForm


# Create your views here.

#services = [
#    {'id': 1, 'name':'Talk about GRIT!!!'},
#    {'id': 2, 'name':'Git/GitHub'},
#    {'id': 3, 'name':'What happens when you type "google.com" in a browser search bar and click enter ?'},
#    {'id': 4, 'name':'Discussion room'},
#]

def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''

    services = Service.objects.filter(topic__name__icontains=q)

    topics = Topic.objects.all()

    context = {'services': services, 'topics': topics}
    return render(request, 'NinazHairline/home.html', context)

def dashboard(request):
    form = SubscribeForm()
    if request.method == 'POST':
        form = SubscribeForm(request.POST)
        if form.is_valid():
            subject = 'Welcome Onboard'
            message = 'Thanks for subscribing to our news feed.\nWe will keep you posted and updated the whole time of the way.\nHosted by Johnson Masino(Back End Developer.)'
            recipient = form.cleaned_data.get('email')
            send_mail(subject, 
              message, settings.EMAIL_HOST_USER, [recipient], fail_silently=False)
            messages.success(request, 'Successfully Sent!')
            return redirect('dashboard')
    context = {'form': form}
    return render(request, 'NinazHairline/dashboard.html', context)

def service(request, pk):
    service = Service.objects.get(id=pk)
    context = {'service': service}

    return render(request, 'NinazHairline/service.html', context)

def createService(request):
    form = ServiceForm()
    if request.method == 'POST':
        form = ServiceForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    context = {'form': form}
    return render(request, 'NinazHairline/service_form.html', context)

def updateService(request, pk):
    service = Service.objects.get(id=pk)
    form = ServiceForm(instance=service)

    if request.method == "POST":
        form = ServiceForm(request.POST, instance=service)
        if form.is_valid():
            form.save()
            return redirect('home')

    context = {'form': form}
    return render(request, 'NinazHairline/service_form.html', context)

def deleteService(request, pk):
    service = Service.objects.get(id=pk)
    if request.method == 'POST':
        service.delete()
        return redirect('home')

    return render(request, 'NinazHairline/delete.html', {'obj': service})


