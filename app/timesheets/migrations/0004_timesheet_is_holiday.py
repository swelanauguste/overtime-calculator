# Generated by Django 4.2.5 on 2023-10-09 14:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('timesheets', '0003_timesheet_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='timesheet',
            name='is_holiday',
            field=models.BooleanField(default=False),
        ),
    ]