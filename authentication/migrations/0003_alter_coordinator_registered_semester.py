# Generated by Django 5.1.2 on 2024-10-10 19:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0002_alter_volunteer_registered_semester'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coordinator',
            name='registered_semester',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
