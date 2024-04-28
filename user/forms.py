from django import forms
from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class FormLogin(forms.Form):
    username = forms.CharField(label="Your account number", max_length=20, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label="Your password", max_length=12, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    # your_name = forms.CharField(label="Your name", max_length=100)

class CustomUserCreationForm(UserCreationForm):
    username = forms.CharField(label="帳號", widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label="信箱",widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(label="密碼",widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label="確認密碼",widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
