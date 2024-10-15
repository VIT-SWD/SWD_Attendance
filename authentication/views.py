from django.shortcuts import render
from django.contrib.auth import login as auth_login, logout, authenticate
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages  
from django.contrib.auth.models import User
from .models import Volunteer, Coordinator, Secretary

def logout_view(request):
    logout(request)
    return redirect('login')

def role_based_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')  
        password = request.POST.get('password')

        try:
            user = User.objects.get(email=email)

            user = authenticate(request, username=user.username, password=password)
        except User.DoesNotExist:
            user = None

        if user is not None:
            auth_login(request, user)  # Log in the user
            
            role = None
            if hasattr(user, 'coordinator'):
                role = 'Coordinator'
            elif hasattr(user, 'volunteer'):
                role = 'Volunteer'
            elif hasattr(user, 'secretary'):
                role = 'Secretary'

            if role == 'Coordinator':
                return redirect('coordinator')  
            elif role == 'Volunteer':
                return redirect('volunteer')  
            elif role == 'Secretary':
                return redirect('secretary') 
            else:
                messages.error(request, "No valid role associated with this user.")
                return redirect('userlogin') 
        else:
            messages.error(request, "Invalid credentials.")
            return redirect('userlogin') 

    return render(request, 'login.html') 


def signup_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        role = request.POST.get('role')
        gender = request.POST.get('gender')
        department = request.POST.get('department')
        div = request.POST.get('div')
        prn = request.POST.get('prn')
        contact = request.POST.get('contact')
        blood_group = request.POST.get('blood_group')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        
        if password1 != password2:
            messages.error(request, "Passwords do not match.")
            return redirect('usersignup')  

        # Create user
        user = User.objects.create_user(username=username, email=email, password=password1)

        if role == 'Volunteer':
            Volunteer.objects.create(
                user=user,
                vname=username,
                email=email,
                gender=gender,
                dept=department,
                div=div,
                prn=prn,
                contact_num=contact,
                blood_group=blood_group
            )
        elif role == 'Coordinator':
            Coordinator.objects.create(
                user=user,
                cname=username,
                email=email,
                gender=gender,
                dept=department,
                div=div,
                prn=prn,
                contact_num=contact,
                blood_group=blood_group
            )
        elif role == 'Secretary':
            Secretary.objects.create(
                user=user,
                sname=username,
                email=email,
                gender=gender,
                dept=department,
                div=div,
                prn=prn,
                contact_num=contact,
                blood_group=blood_group
            )
        else:
            messages.error(request, "Invalid role selected.")
            return redirect('usersignup')

        return redirect('userlogin')

    return render(request, 'login.html')  

def login(request):
    return render(request, 'update.html')

