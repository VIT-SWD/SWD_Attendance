from django.contrib import admin
from authentication.models import Volunteer
from authentication.models import Coordinator
from authentication.models import Secretary
from authentication.models import Activity
from authentication.models import Domain
from authentication.models import Attendance
from authentication.models import FailedRegistration

class VolunteerAdmin(admin.ModelAdmin):
    list_display = ('user','vname', 'email', 'domain', 'activity')
    search_fields=('vname',)
    #fields = (('user','vname'),'email')  to show only selected columns in admin edit
class CoordinatorAdmin(admin.ModelAdmin):
    list_display = ('user','cname', 'email', 'domain', 'activity')
    search_fields=('cname',)
class SecretaryAdmin(admin.ModelAdmin):
    list_display = ('user','sname', 'email', 'domain', 'activity')
    search_fields=('sname',)
class ActivityAdmin(admin.ModelAdmin):
    list_display = ('name','date', 'start_time', 'end_time', 'map_link','isOnline','venue' )
    search_fields=('name',)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('coord_name','vol_name', 'time', 'activity', 'attendance','venue')
    search_fields=('coord_name','vol_name')
class FailedRegistrationAdmin(admin.ModelAdmin):
    list_display = ('name','user_type', 'activity', 'reason', 'time')
    search_fields=('name','user_type','activity')
class DomainAdmin(admin.ModelAdmin):
    list_display = ('name','enabled')
    search_fields=('name',)


# Register your models here.
admin.site.register(Volunteer, VolunteerAdmin)
admin.site.register(Coordinator, CoordinatorAdmin)
admin.site.register(Secretary, SecretaryAdmin)
admin.site.register(Activity,ActivityAdmin)
admin.site.register(Domain,DomainAdmin)
admin.site.register(Attendance,AttendanceAdmin)
admin.site.register(FailedRegistration)