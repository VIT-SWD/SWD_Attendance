from django.contrib import admin
from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.role_based_login, name='userlogin'),
    path('usersignup/', views.signup_view, name='usersignup'),
    
]