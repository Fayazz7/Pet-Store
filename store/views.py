from django.shortcuts import render,redirect,get_object_or_404
from django.views.generic import *
from .forms import *
from . models import *
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse_lazy
from django.db.models import Q

# Create your views here.

class IndexView(View):
    def get(self,request,*args, **kwargs):
        return render (request,"index.html")
     
class SignInView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'signin.html')
    
    def post(self, request, *args, **kwargs):
        form = LogInForm(request.POST)
        if form.is_valid():
            u_name = form.cleaned_data.get("username")
            pwd = form.cleaned_data.get("password")
            user = authenticate(request, username=u_name, password=pwd)
            if user is not None:
                if user.is_superuser:
                    login(request, user)
                    messages.success(request, 'Welcome back, Admin!')
                    return redirect("owner-home")
                else:
                    login(request, user)
                    messages.success(request, 'Login successful! Welcome back!')
                    return redirect("user-home")
            else:
                messages.error(request, 'Invalid username or password.')
                return redirect("sign-in")
        else:
            messages.error(request, 'Invalid form submission. Please try again.')
            return redirect("sign-in")
    
class SignUpView(View):
    def get(self, request, *args, **kwargs):
        form = RegistrationForm()
        return render(request, 'signup.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            user_obj = User.objects.get(username=form.cleaned_data['username'])
            UserProfile.objects.create(user=user_obj, phone=form.cleaned_data['phone_number'])
            messages.success(request, "Registration successful. Please Log-In.")
            return redirect('sign-in')
        else:
            messages.error(request, "Registration failed. Please correct the errors below.")
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
        return render(request, 'signup.html', {'form': form})

class SignOutView(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        messages.success(request, "You have been logged out successfully.")
        return redirect('sign-in')
    
    
class AdminIndexView(View):
    def get(self,request,*args, **kwargs):
        users=Product.objects.all()
        return render (request,'admin-index.html',{"data":users})
    
class UserIndexView(View):
    def get(self, request, *args, **kwargs):
            data = Product.objects.all()
            return render(request, 'user-index.html', {"data":data})
        
    def post(self,request,*args, **kwargs):
        query=request.POST.get('product')
        product_name=Product.objects.filter(title__icontains=query)
        product_category=Product.objects.filter(category__name__icontains=query)
        data=product_name.union(product_category)
        return render(request, 'user-index.html', {"data":data})
        
class CategoryListCreateView(CreateView,ListView):
    template_name="category.html"
    form_class=CategoryForm
    success_url=reverse_lazy("category")
    context_object_name="data"
    model=Category
    
class UserListView(View):
    def get(self,request,*args, **kwargs):
        users=User.objects.all()
        return render (request,'user-list.html',{"data":users})

class DeleteUserView(View):
    def get(self, request, *args, **kwargs):
        id = kwargs.get('pk')
        try:
            user_obj = User.objects.get(id=id)
            user_obj.delete()
            messages.success(request, "User deleted successfully.")
        except User.DoesNotExist:
            messages.error(request, "User does not exist.")
        return redirect('users-list')

    

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
    
class UpdateProductView(View):
    def get(slf,request,*args, **kwargs):
        id=kwargs.get("pk")
        product_obj=get_object_or_404(Product,id=id)
        form=ProductForm(instance=product_obj)
        return render (request,'update-product.html',{"data":form})

    def post(self, request, *args, **kwargs):
        id = kwargs.get("pk")
        product_obj = get_object_or_404(Product, id=id)
        form = ProductForm(request.POST, request.FILES, instance=product_obj)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product was updated successfully.')
            return redirect('update-product', pk=id)
        else:
            messages.error(request, 'There was an error updating the product.')
            return render(request, 'update-product.html', {"data": form})\
                
class AddToCart(View):
    def get(self,request,*args, **kwargs):
        id=kwargs.get("pk")
        product_obj=get_object_or_404(Product,id=id)
        cart_obj=request.user.cart
        if BasketItem.objects.filter(basket=cart_obj,product=product_obj).exists():
                    cart_item_obj=BasketItem.objects.get(basket=cart_obj,product=product_obj)
                    cart_item_obj.quantity+=1
                    product_obj.stock-=1
                    cart_item_obj.save()
                    product_obj.save()
                    messages.success(request, 'Added to Cart.')
                    return redirect('user-home')
        else:
            cart_item_obj=BasketItem.objects.create(basket=cart_obj,product=product_obj)
            product_obj.stock-=1
            product_obj.save()
            cart_item_obj.save()
            messages.success(request, 'Added to Cart.')
            return redirect('user-home')
        
class ViewCart(View):
    def get(self,request,*args, **kwargs):
        cart_item_obj=request.user.cart.cartitem.all()
        cart=Basket.objects.get(owner=request.user)
        return render (request,'cart.html',{"data":cart_item_obj,'cart':cart})
    