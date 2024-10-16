from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
import requests, openpyxl, re
from authentication.models import Activity, Secretary, Volunteer
from django.contrib.auth.decorators import login_required

@login_required(login_url='userlogin')
def secretaryView(request):
    if request.method == 'POST':
        activity = request.POST.get('activity')
        secretary = get_object_or_404(Secretary, user=request.user)
        secretary.activity = activity
        secretary.save()
    else:
        secretary = get_object_or_404(Secretary, user=request.user)
    return render(request, 'secretary.html', {'secretary': secretary})

@login_required(login_url='userlogin')
def add_activity(request):
    if request.method == 'POST':
        activity = request.POST.get('activity')
        eventDate = request.POST.get('event-date')
        startTime = request.POST.get('start-time')
        endTime = request.POST.get('end-time')
        map_link = request.POST.get('map-link')
        description = request.POST.get('description')

        # Extract coordinates from the map_link using regex
        coordinates = extract_coordinates(map_link)
        if coordinates:
            latitude, longitude = coordinates
            print(f"Latitude: {latitude}, Longitude: {longitude}")
        else:
            latitude, longitude = None, None
            print("No coordinates found")
        print(latitude, longitude)

        new_activity = Activity(
            name=activity,
            date=eventDate,
            start_time=startTime,
            end_time=endTime,
            map_link=map_link,
            description=description,
            latitude=float(latitude) if latitude else None,  
            longitude=float(longitude) if longitude else None 
        )
        new_activity.save()

        volunteers = Volunteer.objects.filter(activity=activity)
        for volunteer in volunteers:
            volunteer.attendance += f"#{eventDate.strftime('%d-%m-%Y')}"
            volunteer.save()

        return redirect('secretary')

    return redirect('secretary')

@login_required(login_url='userlogin')
def extract_coordinates(url):
    regex = r'@?([-+]?[\d.]+),([-+]?[\d.]+)'
    expanded_url = expand_url(url)  
    print(f"Expanded URL: {expanded_url}") 
    matches = re.search(regex, expanded_url)

    if matches:
        latitude = matches.group(1)
        longitude = matches.group(2)
        return latitude, longitude
    else:
        return None

def expand_url(short_url):
    try:
        response = requests.head(short_url, allow_redirects=True)
        return response.url  # Return the expanded URL
    except requests.RequestException as e:
        print(f"Error expanding URL: {e}")
        return short_url 
    

def download_attendance(request):
    if request.method == 'POST':
        activity_name = request.POST.get('event-name')
        
        volunteers = Volunteer.objects.filter(activity=activity_name)
        
        workbook = openpyxl.Workbook()
        sheet = workbook.active
        sheet.title = 'Attendance'
        
        headers = ['Name', 'Email', 'PRN', 'Contact No.']
        
        # all_dates = set()
        # for volunteer in volunteers:
        #     attendance_dates = volunteer.attendance.split(', ')
        #     for date_entry in attendance_dates:
        #         date = date_entry[1:] 
        #         all_dates.add(date)
        
        # sorted_dates = sorted(all_dates, key=lambda x: x) 
        all_dates = set()
        for volunteer in volunteers:
            attendance_dates = volunteer.attendance.split(', ')
            for date_entry in attendance_dates:
                if len(date_entry) > 1:  # Ensure the entry is not empty and valid
                    date = date_entry[1:]  # Extract the date, assuming it starts with a special character
                    all_dates.add(date)

        sorted_dates = sorted(all_dates, key=lambda x: x)
        headers.extend(sorted_dates)  
        
        for col_num, header in enumerate(headers, 1):
            sheet.cell(row=1, column=col_num, value=header)
        
        for row_num, volunteer in enumerate(volunteers, start=2):
            sheet.cell(row=row_num, column=1, value=volunteer.vname)
            sheet.cell(row=row_num, column=2, value=volunteer.email)
            sheet.cell(row=row_num, column=3, value=volunteer.prn)
            sheet.cell(row=row_num, column=4, value=volunteer.contact_num)
            
            attendance_status = {}
            attendance_entries = volunteer.attendance.split(', ')
            for entry in attendance_entries:
                status = 'Present' if entry.startswith('$') else 'Absent'
                date = entry[1:] 
                attendance_status[date] = status
            
            for col_num, date in enumerate(sorted_dates, start=5):
                sheet.cell(row=row_num, column=col_num, value=attendance_status.get(date, 'Absent'))

        response = HttpResponse(
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        )
        response['Content-Disposition'] = f'attachment; filename={activity_name}_attendance.xlsx'
        workbook.save(response)
        return response
    else:
        return HttpResponse("Invalid request method.", status=400)

    
