from django.urls import path
from . import views

urlpatterns = [
    path('', views.secretaryView, name='secretary'),
    path('download-attendance/', views.download_attendance, name='download_attendance'),
    path('fetch-div/', views.activityDivisions, name='fetch_div')
]
