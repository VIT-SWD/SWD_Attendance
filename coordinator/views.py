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
    return render(request, 'coordinators.html', {'coordinator': coordinator, 'CURR_YEAR': settings.CURR_YEAR, 'CURR_SEM': settings.CURR_SEM})

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
            qr_codes_dir = os.path.join(settings.STATIC_URL, 'qr_codes/Social_Services/')
        else:
            qr_codes_dir = os.path.join(settings.STATIC_URL, 'qr_codes/Flagship/')

        if not os.path.exists(qr_codes_dir):
            os.makedirs(qr_codes_dir)

        filepath = os.path.join(qr_codes_dir, filename)
        
        img.save(filepath)

        with open(filepath, 'rb') as img_file:
            if request.POST.get('activity'):
                coordinator.qr_codeSS.save(filename, File(img_file), save=True)
            else:
                coordinator.qr_codeFE.save(filename, File(img_file), save=True)

    # return render(request, 'coordinators.html', {'coordinator': coordinator})
    return redirect('coordinator')