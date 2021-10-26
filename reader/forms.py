from django.forms import ModelForm
from .models import News
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class NewsForm(ModelForm):
    class Meta:
        model = News
        fields = '__all__'
        exclude = ['author']
