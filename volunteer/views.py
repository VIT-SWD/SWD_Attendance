from django.shortcuts import render, get_object_or_404, redirect
from authentication.models import Volunteer
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.views import View
from django.utils.decorators import method_decorator
from authentication.models import Attendance, Activity
from datetime import datetime, timedelta
from django.conf import settings
import math
import geopy.distance
from django.utils.timezone import localtime
import json
import requests
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile

@login_required(login_url='userlogin')
def volunteer(request):
    volunteer = get_object_or_404(Volunteer, user=request.user)

    if request.method == 'POST':
        volunteer.roll = request.POST.get('roll')
        volunteer.save()

    activities = [activity for activity in settings.DOMAINS[volunteer.domain] if settings.ACTIVITIES[activity]]

    today = datetime.now().date()

    if today.strftime("%d-%m-%Y") in volunteer.attendance:
        activity_name = volunteer.activity
        idx = 1

        if settings.GROUPS[activity_name]:
            for group in settings.GROUPS[activity_name]:
                min_roll, max_roll = group.split('-')
                min_roll = int(min_roll)
                max_roll = int(max_roll)

                if volunteer.roll >= min_roll and volunteer.roll <= max_roll:
                    div = volunteer.dept + '-' + volunteer.div + '-' + str(idx)
                    events = Activity.objects.filter(name=activity_name, date=today, divisions__icontains=div)
                    break
                idx += 1
        else:
            div = volunteer.dept + '-' + volunteer.div
            events = Activity.objects.filter(name=activity_name, date=today, divisions__icontains=div)
    else:
        events = []

    return render(request, 'volunteers.html', {'volunteer': volunteer, 'CURR_YEAR': settings.CURR_YEAR, 'CURR_SEM': settings.CURR_SEM, 'activities': activities, 'events': events})

@login_required(login_url='userlogin')
def allot_activity(request):
    if request.method == 'POST':
        activity = request.POST.get('activity')
        volunteer = get_object_or_404(Volunteer, user=request.user)
        volunteer.activity = activity
        volunteer.save()
    return redirect('volunteer')

def refresh_access_token():
    global ACCESS_TOKEN
    data = {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "refresh_token": REFRESH_TOKEN,
        "grant_type": "refresh_token"
    }

    response = requests.post(TOKEN_URL, data=data)
    response_data = response.json()

    if "access_token" in response_data:
        ACCESS_TOKEN = response_data["access_token"]
        print("Access token refreshed!")
    else:
        print("Failed to refresh access token:", response_data)
        raise Exception("Token refresh failed")

@method_decorator(csrf_exempt, name='dispatch')
class MarkAttendanceView(LoginRequiredMixin, View):
    login_url = '/userlogin/'

    def post(self, request, *args, **kwargs):
        try:
            coord_prn = request.POST.get('coord_prn')
            coord_name = request.POST.get('coord_name')
            coord_activity = request.POST.get('coord_activity')
            volunteer = get_object_or_404(Volunteer, user=request.user)
            vol_name = volunteer.vname
            vol_prn = volunteer.prn
            actual_latitude = float(request.POST.get('actual_latitude'))
            actual_longitude = float(request.POST.get('actual_longitude'))
            geo_photo = request.FILES.get('geo_photo')
            venue = request.POST.get('venue')

            volunteer = Volunteer.objects.get(user=request.user)

            if geo_photo:
                temp_photo_path = default_storage.save(geo_photo.name, ContentFile(geo_photo.read()))
                print("File saved at:", temp_photo_path)

                # Upload to Google Drive
                file_url = self.upload_to_google_drive(default_storage.path(temp_photo_path), temp_photo_path)
                # print(file_url)

                # Delete the temporary file
                default_storage.delete(temp_photo_path)
            else:
                return JsonResponse({'error': 'Geo photo is required.'}, status=400)

            # current_time = datetime.now().time()
            # today = datetime.now().date()
            current_time = localtime().time()
            today = localtime().date()

            activity_name = volunteer.activity

            if activity_name != coord_activity:
                return JsonResponse({'error': 'The activity of coordinator and volunteer do not match.'}, status=400)

            activities = Activity.objects.filter(name=activity_name, date=today, venue=venue)
            count = activities.count()

            error = ''

            if count == 0:
                return JsonResponse({'error': 'No active activity present to mark attendance.'}, status=400)

            for activity in activities:
                # Time window checks
                in_time_window_start = (datetime.combine(today, activity.start_time) - timedelta(minutes=10)).time()
                in_time_window_end = (datetime.combine(today, activity.start_time) + timedelta(minutes=40)).time()

                out_time_window_start = (datetime.combine(today, activity.end_time) - timedelta(minutes=10)).time()
                out_time_window_end = (datetime.combine(today, activity.end_time) + timedelta(minutes=40)).time()

                if not activity.isOnline:
                    # Calculate distance
                    distance = calculate_distance(
                        actual_latitude, actual_longitude,
                        activity.latitude, activity.longitude
                    )
                    print(distance)

                    # Ensure volunteer is within 1 km range
                    if distance > 3:
                        error = "You are too far from the activity location to mark attendance."
                        continue
                        # return JsonResponse({'error': 'You are too far from the activity location to mark attendance.'}, status=400)

                # In-Time Attendance
                if not volunteer.marked_IN_attendance:
                    if in_time_window_start <= current_time and current_time <= in_time_window_end:
                        # Mark in-time attendance
                        volunteer.marked_IN_attendance = True
                        idx = volunteer.attendance.find(today.strftime("%d-%m-%Y"))
                        volunteer.attendance = volunteer.attendance[:idx-1] + '?' + volunteer.attendance[idx:]
                        # volunteer.attendance += f"{attendance}, "
                        volunteer.save()

                        if file_url == "error":
                            Attendance.objects.create(
                                coord_prn=coord_prn,
                                coord_name=coord_name,
                                activity=activity_name,
                                vol_name=vol_name,
                                vol_prn=vol_prn,
                                actual_latitude=actual_latitude,
                                actual_longitude=actual_longitude,
                                geo_photo=geo_photo,
                                time=datetime.now()
                            )
                        else:
                            Attendance.objects.create(
                                coord_prn=coord_prn,
                                coord_name=coord_name,
                                activity=activity_name,
                                vol_name=vol_name,
                                vol_prn=vol_prn,
                                actual_latitude=actual_latitude,
                                actual_longitude=actual_longitude,
                                geo_photo=file_url,
                                time=datetime.now()
                            )
                        return JsonResponse({'message': 'In-time attendance marked successfully!'}, status=200)
                    else:
                        error = f'Current time is outside the in-time attendance window. {in_time_window_start} - {in_time_window_end} - {activity.venue} - {current_time}'
                        continue
                        # return JsonResponse({'error': 'Current time is outside the in-time attendance window.'}, status=400)
                else:
                    # Out-Time Attendance
                    if current_time >= out_time_window_start and current_time <= out_time_window_end:
                        idx = volunteer.attendance.find(today.strftime("%d-%m-%Y"))

                        if volunteer.attendance[idx-1] == "$":
                            return JsonResponse({'message': 'Your Out-time attendance has already been marked!'}, status=200)

                        volunteer.attendance = volunteer.attendance[:idx-1] + "$" + volunteer.attendance[idx:]
                        # volunteer.marked_IN_attendance = False
                        volunteer.save()

                        # attendance_record = Attendance.objects.get(vol_prn=vol_prn, activity=activity_name)
                        # # attendance_record.marked_IN_attendance = False
                        # attendance_record.save()

                        return JsonResponse({'message': 'Out-time attendance marked successfully!'}, status=200)
                    else:
                        error = 'Current time is outside the out-time attendance window.'
                        continue
                        # return JsonResponse({'error': 'Current time is outside the out-time attendance window.'}, status=400)

            return JsonResponse({'error': error}, status=400)

        except Activity.DoesNotExist:
            return JsonResponse({'error': 'Activity does not exist.'}, status=404)
        except Volunteer.DoesNotExist:
            return JsonResponse({'error': 'Volunteer does not exist.'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    def get(self, request, *args, **kwargs):
        return JsonResponse({'error': 'GET method not allowed.'}, status=405)

    def upload_to_google_drive(self, file_path, file_name):
        access_token = "ya29.a0ARW5m76VxZxdp9AZGNvvyVQ3lAIhh9vRT1LQVW4YblokPir2J4LlGd56sPnDrT_fV_vauhqZRXMMZHTBpbirO0YbCe24_mNG4Q9T_9CxX544c00q52wXIcBRIC-mNv3sYAjs7LIdJ5VSKyU5j_QjDRa0wPpnbCjA4dOncWMBaCgYKAbQSARISFQHGX2Mifx6DvyDdoBYNUc1mv7uOfg0175"
        folder_id = "1PeqgokhAoqYXCQ08jYjtXXFwMEiB-Xq2"  # Replace with drive folder ID

        headers = {"Authorization": f"Bearer {access_token}"}
        para = {
            "name": file_name,
            "parents": [folder_id]
        }
        files = {
            "data": ("metadata", json.dumps(para), "application/json; charset=UTF-8"),
            "file": open(file_path, "rb")
        }
        response = requests.post(
            "https://www.googleapis.com/upload/drive/v3/files?uploadType=multipart",
            headers=headers,
            files=files
        )

        if response.status_code == 200:
            file_id = response.json().get('id')
            return f"https://drive.google.com/file/d/{file_id}/view"
        else:
            # raise Exception(f"Failed to upload to Google Drive: {response.text}")
            return "error"

# def calculate_distance(lat1, lon1, lat2, lon2):
#     lat1_rad = math.radians(lat1)
#     lon1_rad = math.radians(lon1)
#     lat2_rad = math.radians(lat2)
#     lon2_rad = math.radians(lon2)

#     dlon = abs(lon2_rad - lon1_rad)
#     dlat = abs(lat2_rad - lat1_rad)
#     a = math.sin(dlat / 2)*2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon / 2)*2
#     c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
#     distance = 6371 * c
#     return distance

# def calculate_distance(lat1, lon1, lat2, lon2):
#     lat1_rad = math.radians(lat1)
#     lon1_rad = math.radians(lon1)
#     lat2_rad = math.radians(lat2)
#     lon2_rad = math.radians(lon2)

#     dlat = lat2_rad - lat1_rad
#     dlon = lon2_rad - lon1_rad

#     a = math.sin(dlat / 2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon / 2)**2
#     c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

#     distance = 6371 * c
#     return distance

def calculate_distance(lat1, lon1, lat2, lon2):
    coords_1 = (lat1, lon1)
    coords_2 = (lat2, lon2)
    return geopy.distance.geodesic(coords_1, coords_2).km

@login_required(login_url='userlogin')
def view_attendance(request):
    if request.method == 'GET':
        volunteer = get_object_or_404(Volunteer, user=request.user)
        attendance_data = volunteer.attendance

        attendance_list = attendance_data.split(", ")
        parsed_attendance = []

        for entry in attendance_list:
            if entry:
                # status = 'Present' if entry.startswith('$') else 'Absent'
                if entry.startswith('$'):
                    status = 'Present'
                elif entry.startswith('?'):
                    status = 'In-Attendance Marked'
                else:
                    status = 'Absent'
                date = entry[1:]
                parsed_attendance.append({'date': date, 'status': status})

        return JsonResponse({'attendance': parsed_attendance})
