from django.shortcuts import render
from authentication.models import Volunteer, Activity
from django.contrib.auth.models import User
from datetime import date

VERIFICATION_CODE = '202320242025'

def verifyAdmin(request):
    if request.method == 'POST':
        code = request.POST['code']
        if code == VERIFICATION_CODE:
            return render(request, 'delete_vol.html')
        else:
            return render(request, 'admin_login.html', {'message': 'Invalid code'})
    return render(request, 'admin_login.html')

def deleteVolunteer(request):
    if request.method == 'POST':
        email = request.POST['email']
        try:
            user = User.objects.get(username=email)
            volunteer = Volunteer.objects.get(user=user)
            volunteer.delete()
            user.delete()
            return render(request, 'delete_vol.html', {'message': 'Volunteer deleted successfully from both the tables'})
        except:
            return render(request, 'delete_vol.html', {'message': 'Volunteer does not exist'})
    return render(request, 'delete_vol.html')

def onlyVolunteer(request):
    if request.method == 'POST':
        email = request.POST['email']
        try:
            volunteer = Volunteer.objects.get(email=email)
            volunteer.delete()
            return render(request, 'delete_vol.html', {'message': 'Volunteer deleted successfully from Volunteer table'})
        except:
            return render(request, 'delete_vol.html', {'message': 'Volunteer does not exist'})
    return render(request, 'delete_vol.html')

def viewVolunteer(request):
    if request.method == 'POST':
        email = request.POST['email']
        try:
            volunteer = Volunteer.objects.get(email=email)
            return render(request, 'delete_vol.html', {'message': volunteer.vname + ' found'})
        except:
            return render(request, 'delete_vol.html', {'message': 'Volunteer does not exist'})
    return render(request, 'delete_vol.html')

def deleteAttendance(request):
    if request.method == 'POST':
        cutoff_date = date(2024, 12, 31)
        activities_to_delete = Activity.objects.filter(date__lte=cutoff_date)
        activities_to_delete.delete()

        volunteers = Volunteer.objects.all()

        for vol in volunteers:
            if '2025' in vol.attendance:
                vol.attendance = vol.attendance.split('2024, ')[-1]
            else:
                vol.attendance = ''
            vol.save()

        return render(request, 'delete_vol.html', {'message': 'Attendance deleted successfully!'})
    return render(request, 'delete_vol.html')
