# Generated by Django 4.2.16 on 2024-10-12 17:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0012_secretary_flagshipevent'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='activity',
            name='time',
        ),
        migrations.AddField(
            model_name='activity',
            name='end_time',
            field=models.TimeField(null=True),
        ),
        migrations.AddField(
            model_name='activity',
            name='start_time',
            field=models.TimeField(null=True),
        ),
    ]
