
from django.shortcuts import render
from django.contrib import messages
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.conf import settings
from NinazHairline.forms import SubscribeForm


# Create your views here.

def home(request):

    return render(request, 'NinazHairline/index.html')

def dashboard(request):
    form = SubscribeForm()
    if request.method == 'POST':
        form = SubscribeForm(request.POST)
        if form.is_valid():
            subject = 'Code Band'
            message = 'Thanks for subscribing to our news feed.\nWe will keep you posted and updated the whole time of the way.\nHosted by Johnson Masino(Back End Developer.)'
            recipient = form.cleaned_data.get('email')
            send_mail(subject, 
              message, settings.EMAIL_HOST_USER, [recipient], fail_silently=False)
            messages.success(request, 'Successfully Sent!')
            return redirect('dashboard')
    return render(request, 'NinazHairline/dashboard.html', {'form': form})


