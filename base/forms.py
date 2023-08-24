from django.contrib.auth.forms import UserCreationForm
from dataclasses import fields
from pyexpat import model
from django.forms import ModelForm, DateInput
from base.models import  User, BlogPost, Profile
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.http import request
 

class UserSignup(UserCreationForm):
    name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control"
            }
        )
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control"
            }
        )
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control"
            }
        )
    )
    email = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control"
            }
        )
    )

    class Meta:
        model = User
        fields = ['name', 'email','user_type','password1', 'password2']

class UserLoginForm(forms.Form):
    email = forms.CharField(
        widget= forms.TextInput(
            attrs={
                "class": "form-control"
            }
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control"
            }
        )
    )
    class Meta:
       model = User
       fields = ['email', 'password']


class NewpostForm(forms.ModelForm):

    class Meta:
        model = BlogPost
        fields = '__all__'

        exclude = ['created', 'updated']


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = '__all__'
        exclude = ['user']
