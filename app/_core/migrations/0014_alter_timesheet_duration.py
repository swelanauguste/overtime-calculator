# Generated by Django 4.2.5 on 2023-09-25 18:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0013_alter_timesheet_duration'),
    ]

    operations = [
        migrations.AlterField(
            model_name='timesheet',
            name='duration',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=10, null=True),
        ),
    ]