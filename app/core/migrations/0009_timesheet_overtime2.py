# Generated by Django 4.2.5 on 2023-09-25 18:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_remove_timesheet_overtime_rate_delete_overtimerate'),
    ]

    operations = [
        migrations.AddField(
            model_name='timesheet',
            name='overtime2',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=10, null=True),
        ),
    ]
