# Generated by Django 5.1.2 on 2024-10-10 17:28

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Activity',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('domain', models.CharField(max_length=30)),
                ('name', models.CharField(max_length=30)),
                ('enabled', models.BooleanField()),
                ('current_count', models.IntegerField()),
                ('max_count', models.IntegerField()),
                ('flagship_event', models.BooleanField()),
                ('only_males', models.BooleanField()),
                ('only_females', models.BooleanField()),
                ('allotment_done', models.BooleanField(default=True)),
                ('report_filling', models.BooleanField(default=False)),
                ('report_verification', models.BooleanField(default=False)),
                ('t_and_c', models.CharField(max_length=1000, null=True)),
                ('message', models.CharField(default='', max_length=600)),
            ],
            options={
                'verbose_name_plural': 'Activities',
                'ordering': ['-flagship_event', 'name'],
            },
        ),
        migrations.CreateModel(
            name='currentData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('index', models.CharField(max_length=15)),
                ('AcademicYear', models.CharField(max_length=30)),
                ('Semester', models.IntegerField()),
            ],
            options={
                'verbose_name_plural': 'Current-Data',
                'ordering': ['index'],
            },
        ),
        migrations.CreateModel(
            name='Departments',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=70)),
                ('enabled', models.BooleanField()),
            ],
            options={
                'verbose_name_plural': 'Departments',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Domain',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=40)),
                ('enabled', models.BooleanField()),
            ],
            options={
                'verbose_name_plural': 'Domains',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='FailedRegistration',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=50)),
                ('user_type', models.CharField(default='', max_length=30)),
                ('activity', models.CharField(default='', max_length=20)),
                ('reason', models.CharField(default='', max_length=300)),
                ('Time', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name_plural': 'Failed Registrations',
            },
        ),
        migrations.CreateModel(
            name='stats',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('index', models.IntegerField()),
                ('uCount', models.IntegerField()),
                ('vCount', models.IntegerField()),
                ('cCount', models.IntegerField()),
                ('sCount', models.IntegerField()),
                ('totalLogins', models.IntegerField()),
                ('hits', models.IntegerField()),
                ('lastUpdated', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name_plural': 'Stats',
            },
        ),
        migrations.CreateModel(
            name='Coordinator',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cname', models.CharField(max_length=40)),
                ('email', models.EmailField(max_length=30)),
                ('gender', models.CharField(max_length=10)),
                ('dept', models.CharField(max_length=60)),
                ('academic_year', models.CharField(max_length=10)),
                ('registered_academic_year', models.CharField(max_length=30)),
                ('registered_semester', models.IntegerField()),
                ('div', models.CharField(max_length=10)),
                ('prn', models.BigIntegerField()),
                ('contact_num', models.FloatField()),
                ('blood_group', models.CharField(default='', max_length=10)),
                ('activity', models.CharField(max_length=20, null=True)),
                ('flagshipEvent', models.CharField(max_length=30)),
                ('domain', models.CharField(max_length=30, null=True)),
                ('role', models.CharField(default='Coordinator', max_length=20)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Coordinators',
                'ordering': ['cname'],
            },
        ),
        migrations.CreateModel(
            name='Secretary',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sname', models.CharField(max_length=20)),
                ('email', models.EmailField(max_length=30)),
                ('gender', models.CharField(max_length=10)),
                ('dept', models.CharField(max_length=60)),
                ('academic_year', models.CharField(max_length=10)),
                ('registered_academic_year', models.CharField(max_length=30)),
                ('registered_semester', models.IntegerField(default=2)),
                ('domain', models.CharField(max_length=20)),
                ('activity', models.CharField(max_length=20, null=True)),
                ('div', models.CharField(max_length=10)),
                ('prn', models.BigIntegerField()),
                ('blood_group', models.CharField(default='', max_length=10)),
                ('contact_num', models.FloatField()),
                ('role', models.CharField(default='Secretary', max_length=20)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Secretaries',
                'ordering': ['sname'],
            },
        ),
        migrations.CreateModel(
            name='Volunteer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vname', models.CharField(max_length=30)),
                ('email', models.EmailField(max_length=30)),
                ('gender', models.CharField(max_length=10)),
                ('domain', models.CharField(max_length=30)),
                ('activity', models.CharField(max_length=30)),
                ('dept', models.CharField(max_length=60)),
                ('academic_year', models.CharField(max_length=10)),
                ('registered_academic_year', models.CharField(max_length=30)),
                ('registered_semester', models.IntegerField()),
                ('div', models.CharField(max_length=10)),
                ('prn', models.BigIntegerField()),
                ('contact_num', models.FloatField()),
                ('blood_group', models.CharField(default='', max_length=10)),
                ('guardian_faculty', models.CharField(default='not_assigned', max_length=50)),
                ('attendance', models.CharField(default='', max_length=350)),
                ('marked_IN_attendance', models.BooleanField(default=False)),
                ('role', models.CharField(default='Volunteer', max_length=20)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['vname'],
            },
        ),
    ]