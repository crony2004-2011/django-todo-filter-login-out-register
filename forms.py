from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import *

class TaskForm(forms.ModelForm):
    #title= forms.CharField(widget= forms.TextInput(attrs={'placeholder':'Add new task...'}))
    class Meta:
        model = Task
        fields = '__all__'

class CreateuserForm(UserCreationForm):
    class Meta:
        model = User
        #fields = '__all__'
        fields = ['username','password1','email','password2']