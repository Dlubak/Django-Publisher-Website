"""Defines URL patterns for users"""
from django.conf import settings
from django.urls import path, include
from django.contrib.auth import views as auth_view

from . import views

app_name = 'authentication'
urlpatterns = [
    # Include default auth urls.
    path('register/', views.registerPage, name='register'),
    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutPage, name="logout"),
    path('profile/<str:username>', views.profilePage, name='profile'),
    path('profile/<str:username>/edit',
         views.updateProfile, name="update_profile"),
    #path('change_pasword', views.changePasswordPage, name="change_password"),
]
