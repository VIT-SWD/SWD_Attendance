from django.shortcuts import render, redirect, get_object_or_404
from django.core.files import File
import os, qrcode
from django.http import HttpResponse
from django.conf import settings
from authentication.models import Coordinator
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.conf import settings

@login_required(login_url='userlogin')
def coordinator(request):
    coordinator = Coordinator.objects.get(user=request.user)

    if request.method == 'POST':
        coordinator.domain = request.POST.get('domain')
        coordinator.save()

    socialServices = []
    flagships = []

    for activity in settings.ACTIVITIES.keys():
        if settings.ACTIVITIES[activity]:
            if activity in settings.FLAGSHIPS:
                flagships.append(activity)
            else:
                socialServices.append(activity)

    return render(request, 'coordinators.html', {'coordinator': coordinator, 'CURR_YEAR': settings.CURR_YEAR, 'CURR_SEM': settings.CURR_SEM, 'socialServices': socialServices, 'flagships': flagships})

@login_required(login_url='userlogin')
def generate_and_save_qr(request):
    if request.method == 'POST':
        if request.POST.get('activity'):
            activity = request.POST.get('activity')
        else:
            activity = request.POST.get('flagship')

        coordinator = get_object_or_404(Coordinator, user=request.user)

        if request.POST.get('activity'):
            coordinator.activity = activity

            # for dom, acts in settings.DOMAINS.items():
            #     if activity in acts:
            #         coordinator.domain = dom
            #         break
        else:
            coordinator.flagshipEvent = activity
        coordinator.save()

        prn = coordinator.prn
        name = coordinator.cname
        if not prn:
            return HttpResponse("PRN not found", status=400)

        qr = qrcode.QRCode(
            version=5,
            box_size=10,
            border=5
        )

        data = f"PRN: {prn}\nName: {name}\nActivity: {activity}"
        qr.add_data(data)
        qr.make(fit=True)

        img = qr.make_image(fill="black", back_color="white")

        filename = f"{prn}_{activity}.png"
        if request.POST.get('activity'):
            qr_codes_dir = os.path.join(settings.MEDIA_ROOT, 'qr_codes/Social_Services/')
        else:
            qr_codes_dir = os.path.join(settings.MEDIA_ROOT, 'qr_codes/Flagship/')

        if not os.path.exists(qr_codes_dir):
            os.makedirs(qr_codes_dir, exist_ok=True, mode=0o777)

        filepath = os.path.join(qr_codes_dir, filename)

        img.save(filepath)

        with open(filepath, 'rb') as img_file:
            if request.POST.get('activity'):
                coordinator.qr_codeSS.save(filename, File(img_file), save=True)
            else:
                coordinator.qr_codeFE.save(filename, File(img_file), save=True)

    # return render(request, 'coordinators.html', {'coordinator': coordinator})
    return redirect('coordinator')