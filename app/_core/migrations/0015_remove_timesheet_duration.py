# Generated by Django 4.2.5 on 2023-09-25 18:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0014_alter_timesheet_duration'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='timesheet',
            name='duration',
        ),
    ]