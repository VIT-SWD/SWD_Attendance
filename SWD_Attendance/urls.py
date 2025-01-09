from django.contrib import admin
from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static
from authentication import views as auth_views
from coordinator import views as coord_views
from secretary import views as s_views
from volunteer import views as v_views

urlpatterns = [
    path('sasadmin/', admin.site.urls),
    # path('admin/', include('admin_honeypot.urls')),
    # path('admin/', admin.site.urls),
    path('', views.home, name="home"),
    path('profile/', views.profile, name="profile"),
    path('update/', views.update, name="update"),
    path('update_profile/', views.update_profile, name="update_profile"),
    path('coordinator/', include('coordinator.urls')),
    path('userlogin/', include('authentication.urls')),
    path('usersignup/', auth_views.signup_view, name="usersignup"),
    path('secretary/', include('secretary.urls')),
    path('volunteer/', include('volunteer.urls')),
    path('logout/', views.logout_view, name='logout_view'),
    path('add_activity/', s_views.add_activity, name='add_activity'),
    path('allotactivity/', v_views.allot_activity, name="allotactivity"),
    path('mark-attendance/', v_views.MarkAttendanceView.as_view(), name='mark_attendance'),
    path('view_attendance/', v_views.view_attendance, name='view_attendance'),
    path('download-attendance/', s_views.download_attendance, name='download_attendance'),
    path('action/', include('action.urls')),
    path('auth/', include('authentication.urls')),
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
