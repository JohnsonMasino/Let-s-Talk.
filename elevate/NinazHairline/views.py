
from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from NinazHairline.forms import SubscribeForm
from .models import Service, Topic, Message
from .forms import ServiceForm


# Create your views here.

#services = [
#    {'id': 1, 'name':'Talk about GRIT!!!'},
#    {'id': 2, 'name':'Git/GitHub'},
#    {'id': 3, 'name':'What happens when you type "google.com" in a browser search bar and click enter ?'},
#    {'id': 4, 'name':'Discussion room'},
#]

def LoginPage(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == "POST":
        username = request.POST.get('username').lower()
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'User does not exist')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Username Or Password does not exist')

    context = {'page':page}
    return render(request, 'NinazHairline/login_register.html', context)

def LogoutUser(request):
    logout(request)
    return redirect('home')

def registerPage(request):
    form = UserCreationForm()

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'An error occurred when registering')

    return render(request, 'NinazHairline/login_register.html', {'form': form})

def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''

    services = Service.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(description__icontains=q)
        )

    topics = Topic.objects.all()
    service_count = services.count()
    service_messages = Message.objects.filter(Q(service__topic__name__icontains=q))

    context = {'services': services, 'topics': topics,
    'service_count': service_count, 'service_messages': service_messages}
    return render(request, 'NinazHairline/home.html', context)

def dashboard(request):
    form = SubscribeForm()
    if request.method == 'POST':
        form = SubscribeForm(request.POST)
        if form.is_valid():
            subject = 'Welcome Onboard'
            message = 'Thanks for subscribing to our news feed.\nHosted by Johnson Masino(Back End Developer.)'
            recipient = form.cleaned_data.get('email')
            send_mail(subject, 
              message, settings.EMAIL_HOST_USER, [recipient], fail_silently=False)
            messages.success(request, 'Successfully Sent!')
            return redirect('dashboard')
    context = {'form': form}
    return render(request, 'NinazHairline/dashboard.html', context)

def service(request, pk):
    service = Service.objects.get(id=pk)
    service_messages = service.message_set.all().order_by('-created')
    participants = service.participants.all()

    if request.method == 'POST':
        message = Message.objects.create(
            user=request.user,
            service=service,
            body=request.POST.get('body')
        )
        service.participants.add(request.user)
        return redirect('service', pk=service.id)

    context = {'service': service, 'service_messages': service_messages,
               'participants': participants}

    return render(request, 'NinazHairline/service.html', context)

def userProfile(request, pk):
    user = User.objects.get(id=pk)
    services = user.service_set.all()
    service_messages = user.message_set.all()
    topics = Topic.objects.all()
    context = {'user': user, 'services': services,
               'service_messages': service_messages, 'topics': topics}
    return render(request, 'NinazHairline/profile.html', context)

@login_required(login_url='login')
def createService(request):
    form = ServiceForm()
    topics = Topic.objects.all()
    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)

        Service.objects.create(
            host=request.user,
            topic=topic,
            name=request.POST.get('name'),
            description=request.POST.get('description')
        )
        return redirect('home')
    
    context = {'form': form, 'topics': topics}
    return render(request, 'NinazHairline/service_form.html', context)

@login_required(login_url='login')
def updateService(request, pk):
    service = Service.objects.get(id=pk)
    form = ServiceForm(instance=service)
    topics = Topic.objects.all()
    if request.user != service.host:
        return HttpResponse('Sorry you are not the owner!!')

    if request.method == "POST":
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)
        service.name = request.POST.get('name')
        service.topic = topic
        service.description = request.POST.get('description')
        service.save()
        return redirect('home')

    context = {'form': form, 'topics': topics, 'service': service}
    return render(request, 'NinazHairline/service_form.html', context)

@login_required(login_url='login')
def deleteService(request, pk):
    service = Service.objects.get(id=pk)

    if request.user != service.host:
        return HttpResponse('Sorry you are not the owner!!')

    if request.method == 'POST':
        service.delete()
        return redirect('home')

    return render(request, 'NinazHairline/delete.html', {'obj': service})


@login_required(login_url='login')
def deleteMessage(request, pk):
    message = Message.objects.get(id=pk)

    if request.user != message.user:
        return HttpResponse('Sorry you are not the owner!!')

    if request.method == 'POST':
        message.delete()
        return redirect('home')

    return render(request, 'NinazHairline/delete.html', {'obj': message})

def updateUser(request):
    return 