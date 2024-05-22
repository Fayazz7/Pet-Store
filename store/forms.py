from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import *

class RegistrationForm(UserCreationForm):
    phone_number = forms.CharField(max_length=15, required=True, help_text='Required. Enter a valid phone number.')

    class Meta:
        model = User
        fields = ["username", "email", "phone_number", "password1", "password2"]

    def save(self, commit=True):
        user = super().save(commit=False)
        user.phone_number = self.cleaned_data['phone_number']
        if commit:
            user.save()
        return user

class LogInForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField()
    
class CategoryForm(forms.ModelForm):
    class Meta:
        model=Category
        fields=["name"]
        
class ProductForm(forms.ModelForm):
    class Meta:
        model=Product
        fields="__all__"