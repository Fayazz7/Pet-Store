from django.shortcuts import render,redirect,get_object_or_404
from django.views.generic import *
from .forms import *
from . models import *
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse_lazy

# Create your views here.

class IndexView(View):
    def get(self,request,*args, **kwargs):
        
        return render (request,"index.html")
    def post(self,request,*args, **kwargs):
        data=request.POST
        return render (request,"index.html")
     
class SignInView(View):
    def get(self,request,*args, **kwargs):
        return render (request,'signin.html')
    
    def post(self, request, *args, **kwargs):
        form = LogInForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
            u_name = form.cleaned_data.get("username")
            pwd = form.cleaned_data.get("password")
            user = authenticate(request, username=u_name, password=pwd)
            if user.is_superuser:
                login(request, user)
                return redirect("owner-home")
            else:
                login(request, user)
                return redirect("user-home")
        else:
            return redirect("sign-up")
    
class SignUpView(View):
    def get(self, request, *args, **kwargs):
        form = RegistrationForm()
        return render(request, 'signup.html', {'form': form})

    def post(self, request, *args, **kwargs):
        data=request.POST
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            user_obj=User.objects.get(username=data['username'])
            UserProfile.objects.create(user=user_obj,phone=data['phone_number'])
            messages.success(request, "Registration successful. Please Log-In.")
            return render(request, 'signup.html', {'form': form})
        else:
            messages.error(request, "Registration failed. Please correct the errors below.")
        return render(request, 'signup.html', {'form': form})

class SignOutView(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect('sign-in')
    
    
class AdminIndexView(View):
    def get(self,request,*args, **kwargs):
        users=Product.objects.all()
        return render (request,'admin-index.html',{"data":users})
    
class UserIndexView(View):
    def get(self,request,*args, **kwargs):
        return render (request,'user-index.html')
    
class CategoryListCreateView(CreateView,ListView):
    template_name="category.html"
    form_class=CategoryForm
    success_url=reverse_lazy("category")
    context_object_name="data"
    model=Category
    
class ProductListView(View):
    def get(self,request,*args, **kwargs):
        users=Product.objects.all()
        return render (request,'admin-index.html',{"data":users})
    
class CreateProductView(View):
    def get(self, request, *args, **kwargs):
        form = ProductForm()
        return render(request, 'add-product.html', {"form": form})
    
    def post(self, request, *args, **kwargs):
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product was created successfully.')
            return redirect('owner-home')
        else:
            messages.error(request, 'There was an error creating the product.')
            return render(request, 'add-product.html', {"form": form})


class DetailProductView(View):
    def get(self,request,*args, **kwargs):
        id=kwargs.get('pk')
        product_obj=Product.objects.get(id=id)
        return render (request,'view-product.html',{"data":product_obj})
    
class DeleteProductView(View):
    def post(self, request, *args, **kwargs):
        product_id = kwargs.get('pk')
        product = get_object_or_404(Product, id=product_id)
        product.delete()
        messages.success(request, 'Product was deleted successfully.')
        return redirect('owner-home')