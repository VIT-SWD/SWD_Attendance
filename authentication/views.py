from django.shortcuts import render
from django.contrib.auth import login as auth_login, logout, authenticate
from django.shortcuts import render, redirect
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.contrib import messages  
from django.contrib.auth.models import User
from .models import Volunteer, Coordinator, Secretary
import re

def logout_view(request):
    logout(request)
    return redirect('login')

def role_based_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')  
        password = request.POST.get('password')

        try:
            user = User.objects.get(email=email)

            user = authenticate(request, username=email, password=password)
        except User.DoesNotExist:
            user = None

        if user is not None:
            auth_login(request, user)  # Log in the user
            
            role = user.first_name
            # if hasattr(user, 'coordinator'):
            #     role = 'Coordinator'
            # elif hasattr(user, 'volunteer'):
            #     role = 'Volunteer'
            # elif hasattr(user, 'secretary'):
            #     role = 'Secretary'

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
    errors = {}
    form_data = {}
    
    if request.method == 'POST':
        form_data = request.POST
        name = request.POST.get('username')
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

        try:
            validate_email(email)
        except ValidationError:
            errors['email'] = "Invalid email format."

        if not prn.isdigit() or len(prn) != 8:
            errors['prn'] = "PRN must be 8 digits."

        if len(div) != 1 or not div.isalpha():
            errors['div'] = "Division must be a single character."

        if not contact.isdigit() or len(contact) != 10:
            errors['contact'] = "Contact number must be 10 digits."

        if password1 != password2:
            errors['password'] = "Passwords do not match."
        else:
            password_regex = re.compile(r'^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$')
    
            if not password_regex.match(password1):
                errors['password'] = ("Password must be at least 8 characters long, "
                                    "and include at least one uppercase letter, "
                                    "one lowercase letter, one digit, and one special character.")

        required_fields = ['username', 'email', 'role', 'gender', 'department', 'div', 'prn', 'contact', 'blood_group', 'password1', 'password2']
        for field in required_fields:
            if not request.POST.get(field):
                errors[field] = "This field is required."

        if errors:
            return render(request, 'login.html', {'errors': errors, 'form_data': request.POST, 'active_tab': 'signup'})

        # Create user
        user = User.objects.create_user(username=email, password=password1, first_name=role, last_name=name)

        # Create role-based objects
        if role == 'Volunteer':
            Volunteer.objects.create(
                user=user,
                vname=name,
                email=email,
                gender=gender,
                dept=department,
                div=div,
                prn=prn,
                contact_num=contact,
                blood_group=blood_group,
                registered_academic_year='2021-2022',
                registered_semester=2
            )
        elif role == 'Coordinator':
            Coordinator.objects.create(
                user=user,
                cname=name,
                email=email,
                gender=gender,
                dept=department,
                div=div,
                prn=prn,
                contact_num=contact,
                blood_group=blood_group,
                registered_academic_year='2021-2022',
                registered_semester=2
            )
        elif role == 'Secretary':
            Secretary.objects.create(
                user=user,
                sname=name,
                email=email,
                gender=gender,
                dept=department,
                div=div,
                prn=prn,
                contact_num=contact,
                blood_group=blood_group,
                registered_academic_year='2021-2022',
                registered_semester=2
            )
        else:
            messages.error(request, "Invalid role selected.")
            return redirect('usersignup')

        return redirect('userlogin')

    return render(request, 'login.html')


def login(request):
    return render(request, 'update.html')
