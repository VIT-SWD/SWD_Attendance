# Generated by Django 4.2.16 on 2024-10-16 08:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0017_currentdata_alter_volunteer_academic_year'),
    ]

    operations = [
        migrations.DeleteModel(
            name='CurrentData',
        ),
        migrations.AlterField(
            model_name='coordinator',
            name='registered_academic_year',
            field=models.CharField(default='2024-2025', max_length=30),
        ),
        migrations.AlterField(
            model_name='coordinator',
            name='registered_semester',
            field=models.IntegerField(default=1, null=True),
        ),
        migrations.AlterField(
            model_name='secretary',
            name='registered_academic_year',
            field=models.CharField(default='2024-2025', max_length=30),
        ),
        migrations.AlterField(
            model_name='secretary',
            name='registered_semester',
            field=models.IntegerField(default=1, null=True),
        ),
        migrations.AlterField(
            model_name='volunteer',
            name='registered_academic_year',
            field=models.CharField(default='2024-2025', max_length=30),
        ),
        migrations.AlterField(
            model_name='volunteer',
            name='registered_semester',
            field=models.IntegerField(default=1, null=True),
        ),
    ]