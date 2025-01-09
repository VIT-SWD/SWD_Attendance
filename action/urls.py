from django.urls import path
from . import views

urlpatterns = [
    path('', views.verifyAdmin, name='verifyAdmin'),
    path('deleteVol/', views.deleteVolunteer, name='deleteVol'),
    path('onlyVolunteer/', views.onlyVolunteer, name='deleteOnlyVolunteer'),
    path('viewVolunteer/', views.viewVolunteer, name='viewVolunteer'),
    path('deleteAttendance/', views.deleteAttendance, name='deleteAttendance')
]
