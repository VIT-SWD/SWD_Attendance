from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
import requests, openpyxl, re
from authentication.models import Activity, Secretary, Volunteer
from django.contrib.auth.decorators import login_required
from django.conf import settings
from datetime import datetime, date
import json

@login_required(login_url='userlogin')
def secretaryView(request):
    socialServices = []
    flagships = []

    for activity in settings.ACTIVITIES.keys():
        if settings.ACTIVITIES[activity]:
            if activity in settings.FLAGSHIPS:
                flagships.append(activity)
            else:
                socialServices.append(activity)

    if request.method == 'POST':
        secretary = get_object_or_404(Secretary, user=request.user)
        if request.POST.get('domain'):
            secretary.domain = request.POST.get('domain')
        elif request.POST.get('activity'):
            activity = request.POST.get('activity')
            secretary.activity = activity

            # for dom, acts in settings.DOMAINS.items():
            #     if activity in acts:
            #         secretary.domain = dom
            #         break
        else:
            flagshipEvent = request.POST.get('flagship')
            secretary.flagshipEvent = flagshipEvent
        secretary.save()
    else:
        secretary = get_object_or_404(Secretary, user=request.user)

    #filtering events for show event functionality
    # cutoff_date = date(2025, 1, 4)
    cutoff_date = date.today()
    events = []

    if secretary.activity:
        events.extend(Activity.objects.filter(name=secretary.activity, date__gte=cutoff_date))

    if secretary.flagshipEvent:
        events.extend(Activity.objects.filter(name=secretary.flagshipEvent, date__gte=cutoff_date))

    return render(request, 'secretary.html', {'secretary': secretary, 'CURR_YEAR': settings.CURR_YEAR, 'CURR_SEM': settings.CURR_SEM, 'socialServices': socialServices, 'flagships': flagships, 'events': events})

AASHAKIRAN = {
    "CS-L": ["1-16", "17-32", "33-48", "49-64", "65-78"],
    "IT-F": ["1-15", "16-31", "32-47", "48-63", "64-77"]
}

@login_required(login_url='userlogin')
def add_activity(request):
    if request.method == 'POST':
        activity = request.POST.get('activity')
        date_str = request.POST.get('event-date')
        eventDate = datetime.strptime(date_str, '%Y-%m-%d').date()
        startTime = request.POST.get('start-time')
        endTime = request.POST.get('end-time')
        map_link = request.POST.get('map-link')
        description = request.POST.get('description')
        mode = request.POST.get('mode')
        venue = request.POST.get('venue')
        divisions = request.POST.getlist('divisions')
        # print(eventDate)

        # Extract coordinates from the map_link using regex
        coordinates = extract_coordinates(map_link)
        # print(coordinates)
        if coordinates:
            latitude, longitude = coordinates
            print(f"Latitude: {latitude}, Longitude: {longitude}")
        else:
            latitude, longitude = None, None
            print("No coordinates found")
            return JsonResponse({"error": "Invalid Map Link"})
        # print(latitude, longitude)

        new_activity = Activity(
            name=activity,
            date=eventDate,
            start_time=startTime,
            end_time=endTime,
            map_link=map_link,
            description=description,
            latitude=float(latitude) if latitude else None,
            longitude=float(longitude) if longitude else None,
            isOnline = True if mode == 'online' else False,
            venue = venue,
            divisions = str(divisions)[1:-1].replace("'", "")
        )
        new_activity.save()

        #Only for Aashakiran
        if activity == "Aashakiran":
            for div in divisions:
                dept, division, group = div.split('-')
                group = int(group) - 1

                min_roll, max_roll = AASHAKIRAN[dept + '-' + division][group].split('-')
                min_roll = int(min_roll)
                max_roll = int(max_roll)

                volunteers = Volunteer.objects.filter(activity=activity, div=division, dept=dept, roll__range=(min_roll, max_roll))
                for volunteer in volunteers:
                    volunteer.attendance += f"#{eventDate.strftime('%d-%m-%Y')}" + ", "
                    volunteer.save()
            return redirect('secretary')

        for div in divisions:
            if div.count('-') == 1:
                dept, division = div.split('-')
                volunteers = Volunteer.objects.filter(activity=activity, div=division, dept=dept)
                for volunteer in volunteers:
                    volunteer.attendance += f"#{eventDate.strftime('%d-%m-%Y')}" + ", "
                    volunteer.save()
            else:
                dept, division, group = div.split('-')
                group = int(group) - 1

                min_roll, max_roll = settings.GROUPS[activity][group].split('-')
                min_roll = int(min_roll)
                max_roll = int(max_roll)

                volunteers = Volunteer.objects.filter(activity=activity, div=division, dept=dept, roll__range=(min_roll, max_roll))
                for volunteer in volunteers:
                    volunteer.attendance += f"#{eventDate.strftime('%d-%m-%Y')}" + ", "
                    volunteer.save()

        return redirect('secretary')

    return redirect('secretary')

# @login_required(login_url='userlogin')
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

def activityDivisions(request):
    if request.method == 'POST':
        secretary = Secretary.objects.get(user=request.user)
        divisions = []

        if secretary.activity:
            #Only for Aashakiran
            if secretary.activity == "Aashakiran":
                for div in settings.DIVISIONS[secretary.activity]:
                    cnt = 1
                    for group in AASHAKIRAN[div]:
                        divisions.append(div + '-' + str(cnt))
                        cnt += 1
            #After removing 'if' for Aashakiran, make this 'elif' to 'if' and the code will work fine.
            elif len(settings.GROUPS[secretary.activity]) == 0:
                for div in settings.DIVISIONS[secretary.activity]:
                    divisions.append(div)
            else:
                for div in settings.DIVISIONS[secretary.activity]:
                    cnt = 1
                    for group in settings.GROUPS[secretary.activity]:
                        divisions.append(div + '-' + str(cnt))
                        cnt += 1

        if secretary.flagshipEvent:
            if len(settings.GROUPS[secretary.flagshipEvent]) == 0:
                for div in settings.DIVISIONS[secretary.flagshipEvent]:
                    divisions.append(div)
            else:
                for div in settings.DIVISIONS[secretary.flagshipEvent]:
                    cnt = 1
                    for group in settings.GROUPS[secretary.flagshipEvent]:
                        divisions.append(div + '-' + str(cnt))
                        cnt += 1

        return JsonResponse({'divisions': divisions})
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=400)

def updateEvent(request):
    if request.method == 'POST':
        idx = int(request.POST.get('id')) - 1
        venue = request.POST.get('venue')
        startTime = request.POST.get('startTime')
        endTime = request.POST.get('endTime')
        mapLink = request.POST.get('mapLink')

        secretary = get_object_or_404(Secretary, user=request.user)

        # cutoff_date = date(2025, 1, 4)
        cutoff_date = date.today()
        events = []

        if secretary.activity:
            events.extend(Activity.objects.filter(name=secretary.activity, date__gte=cutoff_date))

        if secretary.flagshipEvent:
            events.extend(Activity.objects.filter(name=secretary.flagshipEvent, date__gte=cutoff_date))

        if venue:
            events[idx].venue = venue
        if startTime:
            events[idx].start_time = startTime
        if endTime:
            events[idx].end_time = endTime
        if mapLink:
            events[idx].map_link = mapLink
        events[idx].save()

    return redirect('secretary')

def deleteEvent(request):
    if request.method == 'POST':
        idx = int(request.POST.get('id')) - 1
        secretary = get_object_or_404(Secretary, user=request.user)

        # cutoff_date = date(2025, 1, 4)
        cutoff_date = date.today()
        events = []

        if secretary.activity:
            events.extend(Activity.objects.filter(name=secretary.activity, date__gte=cutoff_date))

        if secretary.flagshipEvent:
            events.extend(Activity.objects.filter(name=secretary.flagshipEvent, date__gte=cutoff_date))

        if events[idx].divisions:
            divisions = events[idx].divisions.split(', ')
        else:
            divisions = []
        eventDate = events[idx].date.strftime('%d-%m-%Y')
        activity = events[idx].name

        events[idx].delete()

        #Only for Aashakiran
        if activity == "Aashakiran":
            for div in divisions:
                dept, division, group = div.split('-')
                group = int(group) - 1

                min_roll, max_roll = AASHAKIRAN[dept + '-' + division][group].split('-')
                min_roll = int(min_roll)
                max_roll = int(max_roll)

                volunteers = Volunteer.objects.filter(activity=activity, div=division, dept=dept, roll__range=(min_roll, max_roll))
                for volunteer in volunteers:
                    index = volunteer.attendance.find(eventDate)
                    if index != -1:
                        volunteer.attendance = volunteer.attendance[:index-1] + volunteer.attendance[index+12:]
                        volunteer.save()
            return redirect('secretary')

        for div in divisions:
            if div.count('-') == 1:
                dept, division = div.split('-')
                volunteers = Volunteer.objects.filter(activity=activity, div=division, dept=dept)
                for volunteer in volunteers:
                    index = volunteer.attendance.find(eventDate)
                    if index != -1:
                        volunteer.attendance = volunteer.attendance[:index-1] + volunteer.attendance[index+12:]
                        volunteer.save()
            else:
                dept, division, group = div.split('-')
                group = int(group) - 1

                min_roll, max_roll = settings.GROUPS[activity][group].split('-')
                min_roll = int(min_roll)
                max_roll = int(max_roll)

                volunteers = Volunteer.objects.filter(activity=activity, div=division, dept=dept, roll__range=(min_roll, max_roll))
                for volunteer in volunteers:
                    index = volunteer.attendance.find(eventDate)
                    if index != -1:
                        volunteer.attendance = volunteer.attendance[:index-1] + volunteer.attendance[index+12:]
                        volunteer.save()
    return redirect('secretary')

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
        # all_dates = []
        # if volunteers:
        #     attendance_dates = volunteers[0].attendance.split(', ')
        #     for date_entry in attendance_dates:
        #         if len(date_entry) > 1:  # Ensure the entry is not empty and valid
        #             date = date_entry[1:]  # Extract the date, assuming it starts with a special character
        #             all_dates.append(date)

        all_dates = []
        events = Activity.objects.filter(name=activity_name)

        for event in events:
            evt_date = '-'.join(str(event.date).split('-')[::-1])
            if evt_date not in all_dates:
                all_dates.append(evt_date)

        # sorted_dates = sorted(all_dates, key=lambda x: x)
        headers.extend(all_dates)

        for col_num, header in enumerate(headers, 1):
            sheet.cell(row=1, column=col_num, value=header)

        for row_num, volunteer in enumerate(volunteers, start=2):
            sheet.cell(row=row_num, column=1, value=volunteer.vname)
            sheet.cell(row=row_num, column=2, value=volunteer.email)
            sheet.cell(row=row_num, column=3, value=volunteer.prn)
            sheet.cell(row=row_num, column=4, value=volunteer.contact_num)

            attendance_status = {}
            attendance = volunteer.attendance
            # for entry in attendance_entries:
            #     status = 'Present' if entry.startswith('$') else 'Absent'
            #     date = entry[1:]
            #     attendance_status[date] = status
            for entry in all_dates:
                idx = attendance.find(entry)

                if idx == -1:
                    status = 'NA'
                elif attendance[idx-1] == '$':
                    status = 'Present'
                else:
                    status = 'Absent'

                attendance_status[entry] = status

            for col_num, date in enumerate(all_dates, start=5):
                sheet.cell(row=row_num, column=col_num, value=attendance_status.get(date, 'Absent'))

        response = HttpResponse(
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        )
        response['Content-Disposition'] = f'attachment; filename={activity_name}_attendance.xlsx'
        workbook.save(response)
        return response
    else:
        return HttpResponse("Invalid request method.", status=400)
