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
urlpatterns = [
    path('admin/', admin.site.urls),
    path('',IndexView.as_view(),name='index'),
    path('login/',SignInView.as_view(),name='sign-in'),
    path('register/',SignUpView.as_view(),name='sign-up'),
    path('owner/', AdminIndexView.as_view(), name='owner-home'),
    path('user/',UserIndexView.as_view(), name='user-home'),
    path('logout',SignOutView.as_view(), name='sign-out'),
    path('users/list/',UsersListView.as_view(),name='users-list')
]
