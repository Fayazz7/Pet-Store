"""
URL configuration for petstore project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from store.views import *
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('admin/', admin.site.urls),
    path('',IndexView.as_view(),name='index'),
    path('login/',SignInView.as_view(),name='sign-in'),
    path('register/',SignUpView.as_view(),name='sign-up'),
    path('owner/', AdminIndexView.as_view(), name='owner-home'),
    path('user/',UserIndexView.as_view(), name='user-home'),
    path('logout',SignOutView.as_view(), name='sign-out'),
    path('users/list/',UserListView.as_view(),name='users-list'),
    path('user/delete/<int:pk>/',DeleteUserView.as_view(),name='delete-user'),
    path('product/add/',CreateProductView.as_view(),name='add-product'),
    path('category/',CategoryListCreateView.as_view(),name='category'),
    path('product/view/<int:pk>/',DetailProductView.as_view(),name='view-product'),
    path('product/delete/<int:pk>/',DeleteProductView.as_view(),name='delete-product'),
    path('product/update/<int:pk>/',UpdateProductView.as_view(),name='update-product'),
    path('cart/add/<int:pk>/',AddToCart.as_view(),name='add-to-cart'),
    path('cart/view/',ViewCart.as_view(),name='view-cart'),
    path('cart/remove/<int:pk>',RemoveFromCart.as_view(),name='remove-item'),
    path('complaint/add/',CreateComplaint.as_view(),name='create-complaint'),
    path('complaint/view',ViewComplaints.as_view(),name='view-complaints'),
    path('complaint/delete/<int:pk>',DeleteComplaint.as_view(),name='delete-complaint'),
    path('order/view/',OrderView.as_view(),name='order-view'),
    path('order/create/',CreateOrder.as_view(),name='order-create'),
    path('order/cancel/<int:pk>/',CancelOrder.as_view(),name='cancel-order'),
    path('order/update/status/<int:pk>/',UpdateOrderStatus.as_view(),name='update-status')
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
