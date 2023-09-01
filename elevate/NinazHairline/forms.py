
from django import forms
from django.forms import ModelForm
from .models import Service


class SubscribeForm(forms.Form):
    email = forms.EmailField()

class ServiceForm(ModelForm):
    class Meta:
        model = Service
        fields = '__all__'
        exclude = ['host', 'partricipants']

