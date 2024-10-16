from django.shortcuts import render, get_object_or_404
from authentication.models import Volunteer
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.views import View
from django.utils.decorators import method_decorator
from authentication.models import Attendance, Activity
from datetime import datetime, timedelta

@login_required(login_url='userlogin')
def volunteer(request):
    return render(request, 'volunteers.html')

@login_required(login_url='userlogin')
def allot_activity(request):
    if request.method == 'POST':
        activity = request.POST.get('activity')
        volunteer = get_object_or_404(Volunteer, user=request.user)
        volunteer.activity = activity
        volunteer.save()
    else:
        volunteer = get_object_or_404(Volunteer, user=request.user)
    return render(request, 'volunteers.html', {'volunteer': volunteer})

@method_decorator(csrf_exempt, name='dispatch')
class MarkAttendanceView(LoginRequiredMixin, View):
    login_url = '/userlogin/' 
    
    def post(self, request, *args, **kwargs):
        try:
            coord_prn = request.POST.get('coord_prn')
            coord_name = request.POST.get('coord_name')
            volunteer = get_object_or_404(Volunteer, user=request.user)
            vol_name = volunteer.vname
            vol_prn = volunteer.prn
            actual_latitude = float(request.POST.get('actual_latitude'))
            actual_longitude = float(request.POST.get('actual_longitude'))
            geo_photo = request.FILES.get('geo_photo')
            
            volunteer = Volunteer.objects.get(user_id=vol_prn)
            
            activity_name = volunteer.activity
            activity = Activity.objects.get(name=activity_name)
            print(activity_name)
            print(activity)


            current_time = datetime.now().time()
            print(current_time)

            
            today = datetime.now().date()
            print(today)
            if today != activity.date:
                return JsonResponse({'error': 'Attendance can only be marked on the activity date.'}, status=400)

            # Time window checks
            in_time_window_start = (datetime.combine(today, activity.start_time) - timedelta(minutes=10)).time()
            in_time_window_end = (datetime.combine(today, activity.start_time) + timedelta(minutes=40)).time()

            out_time_window_start = (datetime.combine(today, activity.end_time) - timedelta(minutes=10)).time()
            out_time_window_end = (datetime.combine(today, activity.end_time) + timedelta(minutes=40)).time()

            # Calculate distance
            distance = calculate_distance(
                actual_latitude, actual_longitude,
                activity.latitude, activity.longitude
            )
            print(actual_latitude, actual_longitude,
                activity.latitude, activity.longitude)
            print(distance)

            # Ensure volunteer is within 1 km range
            if distance > 1000:
                return JsonResponse({'error': 'You are too far from the activity location to mark attendance.'}, status=400)


            # In-Time Attendance
            if not volunteer.marked_IN_attendance:
                if in_time_window_start <= current_time <= in_time_window_end:
                    # Mark in-time attendance
                    volunteer.marked_IN_attendance = True
                    # volunteer.attendance += f"{attendance}, "
                    volunteer.save()

                    Attendance.objects.create(
                        coord_prn=coord_prn,
                        coord_name=request.POST.get('coord_name'),
                        activity=activity_name,
                        vol_name=vol_name,
                        vol_prn=vol_prn,
                        actual_latitude=actual_latitude,
                        actual_longitude=actual_longitude,
                        geo_photo=geo_photo,
                        time=datetime.now()
                    )
                    return JsonResponse({'message': 'In-time attendance marked successfully!'}, status=200)
                else:
                    return JsonResponse({'error': 'Current time is outside the in-time attendance window.'}, status=400)
            else:
                # Out-Time Attendance
                if out_time_window_start <= current_time <= out_time_window_end:
                    # Mark out-time attendance
                    # attendance = f"${today.strftime('%d-%m-%Y')}"
                    volunteer.attendance[-13] = "$"
                    volunteer.save()

                    attendance_record = Attendance.objects.get(vol_prn=vol_prn, activity=activity_name)
                    attendance_record.marked_IN_attendance = False
                    attendance_record.save()

                    return JsonResponse({'message': 'Out-time attendance marked successfully!'}, status=200)
                else:
                    return JsonResponse({'error': 'Current time is outside the out-time attendance window.'}, status=400)

        except Activity.DoesNotExist:
            return JsonResponse({'error': 'Activity does not exist.'}, status=404)
        except Volunteer.DoesNotExist:
            return JsonResponse({'error': 'Volunteer does not exist.'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    def get(self, request, *args, **kwargs):
        return JsonResponse({'error': 'GET method not allowed.'}, status=405)


import math
def calculate_distance(lat1, lon1, lat2, lon2):
    lat1_rad = math.radians(lat1)
    lon1_rad = math.radians(lon1)
    lat2_rad = math.radians(lat2)
    lon2_rad = math.radians(lon2)

    dlon = lon2_rad - lon1_rad
    dlat = lat2_rad - lat1_rad
    a = math.sin(dlat / 2)*2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon / 2)*2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distance = 6371 * c
    return distance

@login_required(login_url='userlogin')
def view_attendance(request):
    if request.method == 'GET':
        volunteer = get_object_or_404(Volunteer, user=request.user)
        attendance_data = volunteer.attendance

        attendance_list = attendance_data.split(", ")
        parsed_attendance = []
        
        for entry in attendance_list:
            if entry:
                status = 'Present' if entry.startswith('$') else 'Absent'
                date = entry[1:] 
                parsed_attendance.append({'date': date, 'status': status})


        return JsonResponse({'attendance': parsed_attendance})