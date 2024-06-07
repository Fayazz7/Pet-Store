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
        model = Product
        fields = ['title', 'picture', 'price', 'description', 'stock', 'category']
        
class ComplaintForm(forms.ModelForm):
    class Meta:
        model=Complaints
        fields="__all__"
        
class OrderForm(forms.Form):
    class Meta:
        model=Order
        fields=['user','product','quantity','order_status','total']
        
class UpdateProfileForm(forms.ModelForm):
    phone = forms.CharField(max_length=20, required=True)

    class Meta:
        model = User
        fields = ['username', 'email']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(UpdateProfileForm, self).__init__(*args, **kwargs)
        if user:
            self.fields['username'].initial = user.username
            self.fields['email'].initial = user.email
            self.fields['phone'].initial = user.profile.phone

    def save(self, commit=True):
        user = super(UpdateProfileForm, self).save(commit=False)
        user.profile.phone = self.cleaned_data['phone']
        if commit:
            user.save()
            user.profile.save()
        return user