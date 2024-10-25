from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, update_session_auth_hash
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from authentication.models import Volunteer, Coordinator, Secretary

def home(request):
    return redirect('userlogin')

@login_required(login_url='userlogin')
def update(request):
    return render(request, 'update.html')

def logout_view(request):
    logout(request)
    return redirect('userlogin')

@login_required(login_url='userlogin')
def profile(request):
    user = request.user 
    
    role_info = None
    if hasattr(user, 'volunteer'):
        role_info = user.volunteer
    elif hasattr(user, 'coordinator'):
        role_info = user.coordinator
    elif hasattr(user, 'secretary'):
        role_info = user.secretary

    context = {
        'user': user,
        'role_info': role_info,
    }
    return render(request, 'profile.html', context)

@login_required(login_url='userlogin')
def update_profile(request):
    user = request.user       
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        old_pass = request.POST.get('old_pass')
        new_pass = request.POST.get('new_pass')
        c_pass = request.POST.get('c_pass')
        profile_pic = request.FILES.get('profile_pic')


        if user.check_password(old_pass):
            user.username = email
            user.last_name = name
            
            if new_pass:
                if new_pass == c_pass:
                    user.set_password(new_pass)
                    user.save()
                    update_session_auth_hash(request, user)
                else:
                    messages.error(request, 'New passwords do not match.')
                    return redirect('update')

            if profile_pic:
                if user.first_name == 'Volunteer':
                    volunteer = Volunteer.objects.get(user=user)
                    volunteer.profile_picture = profile_pic
                    volunteer.save()
                elif user.first_name == 'Coordinator':
                    coordinator = Coordinator.objects.get(user=user)
                    coordinator.profile_picture = profile_pic
                    coordinator.save()
                elif user.first_name == 'Secretary':
                    secretary = Secretary.objects.get(user=user)
                    secretary.profile_picture = profile_pic
                    secretary.save()

            user.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('update')
        else:
            messages.error(request, 'Old password is incorrect.')

    return render(request, 'profile.html')
