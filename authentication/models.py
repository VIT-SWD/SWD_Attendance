from django.db import models
from django.contrib.auth.models import User

class Volunteer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    vname = models.CharField(max_length=30)
    email = models.EmailField(max_length=30)
    gender = models.CharField(max_length=10)
    domain = models.CharField(max_length=30)
    activity = models.CharField(max_length=30, default='')
    dept = models.CharField(max_length=60)
    academic_year = models.CharField(max_length=10, default='FY')
    registered_academic_year = models.CharField(max_length=30, default='2024-2025')
    registered_semester = models.IntegerField(null=True, default=1)
    div = models.CharField(max_length=10)
    prn = models.BigIntegerField()
    contact_num = models.FloatField()
    blood_group = models.CharField(max_length=10, default='')
    guardian_faculty = models.CharField(max_length=50, default='not_assigned')
    attendance = models.CharField(max_length=350, default='')
    marked_IN_attendance = models.BooleanField(default=False)
    # role = models.CharField(max_length=20, default='Volunteer')
    profile_picture = models.ImageField(upload_to='static/profile_pictures', default='default-profile.jpg')
    def str(self):
        return self.vname
    class Meta:
        ordering = ['vname']

class Coordinator(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    cname = models.CharField(max_length=40)
    email = models.EmailField(max_length=30)
    gender = models.CharField(max_length=10)
    dept = models.CharField(max_length=60)
    academic_year = models.CharField(max_length=10)
    registered_academic_year = models.CharField(max_length=30, default='2024-2025')
    registered_semester = models.IntegerField(null=True, default=1)
    div = models.CharField(max_length=10)
    prn = models.BigIntegerField()
    contact_num = models.FloatField()
    blood_group = models.CharField(max_length=10, default='')
    activity = models.CharField(max_length=20, null=True)
    flagshipEvent = models.CharField(max_length=30)
    domain = models.CharField(max_length=30, null=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', default='default-profile.jpg')
    qr_codeSS = models.ImageField(upload_to='qr_codes/Social_Services/', null=True, blank=True)
    qr_codeFE = models.ImageField(upload_to='qr_codes/Flagship/', null=True, blank=True)
    # role = models.CharField(max_length=20, default='Coordinator')
    def _str_(self):
        return self.cname
    class Meta:
        verbose_name_plural = 'Coordinators'
        ordering = ['cname']

class Secretary(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    sname = models.CharField(max_length=20)
    email = models.EmailField(max_length=30)
    gender = models.CharField(max_length=10)
    dept = models.CharField(max_length=60)
    academic_year = models.CharField(max_length=10)
    registered_academic_year = models.CharField(max_length=30, default='2024-2025')
    registered_semester = models.IntegerField(null=True, default=1)
    domain = models.CharField(max_length=20)
    flagshipEvent = models.CharField(max_length=30, null=True)
    activity = models.CharField(max_length=20, null = True)
    div = models.CharField(max_length=10)
    prn = models.BigIntegerField()
    blood_group = models.CharField(max_length=10, default='')
    contact_num = models.FloatField()
    profile_picture = models.ImageField(upload_to='static/profile_pictures', default='default-profile.jpg')
    # role = models.CharField(max_length=20, default='Secretary')
    def _str_(self):
        return self.sname
    class Meta:
        verbose_name_plural = 'Secretaries'
        ordering = ['sname']

class Activity(models.Model):
    name = models.CharField(max_length=255, null=True)  
    date = models.DateField(null=True)                 
    start_time = models.TimeField(null=True)
    end_time = models.TimeField(null=True)              
    map_link = models.URLField(max_length=2000, null=True, blank=True) 
    description = models.TextField(blank=True, null=True) 
    latitude = models.FloatField(null=True)            
    longitude = models.FloatField(null=True)      
    def __str__(self):
        return self.name

class FailedRegistration(models.Model):
    name = models.CharField(max_length=50, default='')
    user_type = models.CharField(max_length=30, default='')
    activity = models.CharField(max_length=20, default='')
    reason = models.CharField(max_length=300, default='')
    Time = models.DateTimeField(auto_now_add=True)
    class Meta:
        verbose_name_plural = 'Failed Registrations'


class Domain(models.Model):
    name = models.CharField(max_length=40)
    enabled = models.BooleanField()
    def _str_(self):
        return self.name
    class Meta:
        verbose_name_plural = 'Domains'
        ordering =  ['name']


class Attendance(models.Model):
    coord_name = models.CharField(max_length=100, null=True, blank=True)
    coord_prn = models.CharField(max_length=20, null=True, blank=True)
    vol_name = models.CharField(max_length=100, null=True, blank=True)
    vol_prn = models.CharField(max_length=20, null=True, blank=True)
    geo_photo = models.ImageField(upload_to='geophotos/', null=True, blank=True)
    actual_latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    actual_longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    time = models.DateTimeField(auto_now_add=True)
    activity = models.CharField(max_length=50, null=True)
    attendance = models.CharField(max_length=350, default='')
    marked_IN_attendance = models.BooleanField(default=False)
